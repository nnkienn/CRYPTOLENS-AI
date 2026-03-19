from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from config.settings import settings

# Tạo engine kết nối Async
engine = create_async_engine(settings.DATABASE_URL, echo=True)

# Tạo Session để thao tác với DB
AsyncSessionLocal = sessionmaker(
    engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

# Base class để các models kế thừa
Base = declarative_base()

# Dependency để inject vào FastAPI routes
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session