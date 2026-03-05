from fastapi import FastAPI

app = FastAPI(
    title="My API",
    description="A simple API built with FastAPI"
)
@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}