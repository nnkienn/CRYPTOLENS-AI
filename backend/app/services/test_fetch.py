from fastapi import FastApi
from datetime import datetime 


app = FastApi(
    title="Test Fetch API",
    description ="API for testing fetch functionality",
    version="1.0.0",
)
async def health_check():
    """
    Kiểm tra trạng thái hệ thống
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "database": "connected (mock)",
            "vector_db": "ready (mock)",
            "redis": "ready (mock)"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)