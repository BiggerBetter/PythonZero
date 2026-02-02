import mlx_whisper
from fastapi import FastAPI, WebSocket

app = FastAPI()

# 加载模型到 M1 Max GPU
MODEL_PATH = "mlx-community/whisper-large-v3-turbo"


@app.websocket("/ws/stt")
async def speech_to_text(websocket: WebSocket):
    await websocket.accept()
    audio_buffer = bytearray()

    # 设置一个 3 秒的静音计数器
    silence_counter = 0

    while True:
        data = await websocket.receive_bytes()
        audio_buffer.extend(data)

        # 实时转写
        result = mlx_whisper.transcribe(audio_buffer, path_or_hf_repo=MODEL_PATH)
        text = result['text']

        # 发送中间结果给前端展示
        await websocket.send_json({"text": text, "is_final": False})

        # 结尾逻辑判断
        if "说完了" in text or "完毕" in text:
            await websocket.send_json({"text": text, "is_final": True})
            audio_buffer.clear()  # 确认结束，清空缓冲