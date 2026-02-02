import json

from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import Utils.env_setup
import ollama

app = FastAPI(title="Local Ollama API")

# 定义前端传来的数据结构
class ChatRequest(BaseModel):
    model: str = "gpt-oss:20b"  # 默认使用 lgpt-oss:20b
    prompt: str
    system_prompt: str = "你是一个专业的人工智能助手。"


@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        # 打印一下接收到的数据，方便调试
        print(f"正在调用模型: {request.model}, 内容: {request.prompt}")

        response = ollama.generate(
            model=request.model,
            prompt=request.prompt,
            system=request.system_prompt
        )

        print("response:", response['response'])
        return {"response": response['response']}
    except ollama.ResponseError as e:
        # 如果是 Ollama 内部错误（比如模型找不到）
        print(f"Ollama 错误: {e.error}")
        raise HTTPException(status_code=e.status_code, detail=e.error)
    except Exception as e:
        # 其他 Python 错误
        print(f"系统错误: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    """
    流式调用：像 ChatGPT 一样逐字返回，前端体验更好
    """
    def generate():
        try:
            stream = ollama.generate(
                model=request.model,
                prompt=request.prompt,
                system=request.system_prompt,
                stream=True
            )
            for chunk in stream:
                # 提取生成的文本片段
                content = chunk['response']
                # 按照 Server-Sent Events (SSE) 格式或其他自定义格式输出
                yield content
        except Exception as e:
            yield f"Error: {str(e)}"

    return StreamingResponse(generate(), media_type="text/plain")

if __name__ == "__main__":
    import uvicorn
    # 启动服务，监听 8000 端口
    uvicorn.run(app, host="0.0.0.0", port=8000)