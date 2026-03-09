from fastapi import FastAPI
from datetime import datetime
import asyncio

app = FastAPI(title="CryptoLens AI")

@app.get("/health")
async def health_check():
    """
    Endpoint kiểm tra trạng thái hệ thống. 
    Sau này sẽ dùng để check kết nối DB, Redis, v.v.
    """
    return {
        "status": "active",
        "timestamp": datetime.now().isoformat(),
        "version": "1.1",
        "engine": "FastAPI + Asyncio"
    }

# Cách chạy trực tiếp nếu không muốn gõ uvicorn ngoài terminal
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8080, reload=True)