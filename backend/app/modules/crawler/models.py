from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field
import sqlalchemy as sa

# 1. Base Schema: Những thứ cơ bản nhất
class ArticleBase(SQLModel):
    title: str = Field(index=True)
    content: str
    url: str = Field(unique=True, index=True)
    source: Optional[str] = None
    author: Optional[str] = None
    published_at: Optional[datetime] = None

# 2. Table Model: Đại diện cho bảng 'article' trong Postgres
class Article(ArticleBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Các trường phục vụ hệ thống AI/Crawler
    status: str = Field(default="raw")  # raw, processing, completed, error
    is_embedded: bool = Field(default=False)
    
    # Tự động ghi nhận thời gian
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=sa.Column(sa.DateTime(timezone=True), server_default=sa.func.now())
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=sa.Column(sa.DateTime(timezone=True), onupdate=sa.func.now())
    )

# 3. Schema để dùng trong API (Data Transfer Object)
class ArticleCreate(ArticleBase):
    pass

class ArticleRead(ArticleBase):
    id: int
    created_at: datetime