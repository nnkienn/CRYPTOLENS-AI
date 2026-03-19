from fastapi import FastAPI
from app.core.database import engine
from sqlmodel import SQLModel

# QUAN TRỌNG: Ông phải import các Model vào đây 
# thì SQLModel mới biết đường mà tạo bảng
from app.modules.auth import models as auth_models
from app.modules.crawler import models as crawler_models

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    # Lệnh này sẽ tự động tạo Schema và Bảng trong Postgres
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    print("🚀 Database đã được khởi tạo: Các bảng User và Article đã sẵn sàng!")

@app.get("/")
async def root():
    return {"message": "CryptoLens AI is Running"}