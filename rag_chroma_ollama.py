import os
import glob
import hashlib
from typing import List, Dict

import chromadb
import ollama

# ====== 配置区 ======
CHROMA_DIR = "./chroma_db"
COLLECTION_NAME = "docs"
EMBED_MODEL = "nomic-embed-text"
CHAT_MODEL = "llama3.2"   # 你本地有啥就填啥，比如 llama3, qwen2.5, mistral 等
DATA_DIR = "./data"      # 把你的 txt/md 放这里
CHUNK_SIZE = 800         # 字符数切分（实验阶段足够）
CHUNK_OVERLAP = 120
TOP_K = 5
# ====================


def read_text_file(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def chunk_text(text: str, chunk_size: int, overlap: int) -> List[str]:
    text = text.strip()
    if not text:
        return []
    chunks = []
    start = 0
    step = max(1, chunk_size - overlap)
    while start < len(text):
        end = min(len(text), start + chunk_size)
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start += step
    return chunks


def stable_id(source: str, idx: int, chunk: str) -> str:
    h = hashlib.sha256(f"{source}::{idx}::{chunk}".encode("utf-8")).hexdigest()
    return h[:32]


def embed_texts(texts: List[str]) -> List[List[float]]:
    # ollama.embeddings 返回 {"embedding": [...]}
    vectors = []
    for t in texts:
        r = ollama.embeddings(model=EMBED_MODEL, prompt=t)
        vectors.append(r["embedding"])
    return vectors


def build_collection():
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )
    return collection


def ingest():
    collection = build_collection()

    paths = []
    paths += glob.glob(os.path.join(DATA_DIR, "**/*.txt"), recursive=True)
    paths += glob.glob(os.path.join(DATA_DIR, "**/*.md"), recursive=True)

    if not paths:
        print(f"[ingest] No .txt/.md files found in {DATA_DIR}")
        return

    docs, metadatas, ids = [], [], []

    for p in paths:
        text = read_text_file(p)
        chunks = chunk_text(text, CHUNK_SIZE, CHUNK_OVERLAP)
        for i, c in enumerate(chunks):
            ids.append(stable_id(p, i, c))
            docs.append(c)
            metadatas.append({"source": p, "chunk_index": i})

    # 批量 embedding（简单起见这里逐条 embed；数据大了可以自己做批处理/并发）
    print(f"[ingest] Embedding {len(docs)} chunks...")
    vectors = embed_texts(docs)

    # upsert
    collection.upsert(
        ids=ids,
        documents=docs,
        metadatas=metadatas,
        embeddings=vectors,
    )
    print(f"[ingest] Done. Collection size now: {collection.count()}")


def retrieve(query: str) -> List[Dict]:
    collection = build_collection()
    qvec = ollama.embeddings(model=EMBED_MODEL, prompt=query)["embedding"]

    res = collection.query(
        query_embeddings=[qvec],
        n_results=TOP_K,
        include=["documents", "metadatas", "distances"],
    )

    out = []
    for doc, meta, dist in zip(res["documents"][0], res["metadatas"][0], res["distances"][0]):
        out.append({"text": doc, "meta": meta, "distance": dist})
    return out


def rag_answer(question: str) -> str:
    hits = retrieve(question)
    context = "\n\n---\n\n".join(
        [f"[source: {h['meta']['source']} | chunk: {h['meta']['chunk_index']}]\n{h['text']}" for h in hits]
    )

    prompt = f"""你是一个严谨的助手。只能基于给定的资料回答。
如果资料不足，请明确说“资料不足”，并指出缺了什么信息。

资料：
{context}

问题：{question}
答案："""

    r = ollama.generate(model=CHAT_MODEL, prompt=prompt)
    return r["response"]


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--ingest", action="store_true", help="Ingest files from ./data into Chroma")
    parser.add_argument("--q", type=str, default="", help="Question for retrieval/RAG")
    parser.add_argument("--mode", type=str, default="rag", choices=["retrieve", "rag"])
    args = parser.parse_args()

    if args.ingest:
        ingest()

    if args.q:
        if args.mode == "retrieve":
            hits = retrieve(args.q)
            for i, h in enumerate(hits, 1):
                print(f"\n#{i} distance={h['distance']:.4f} meta={h['meta']}\n{h['text'][:600]}")
        else:
            print(rag_answer(args.q))
