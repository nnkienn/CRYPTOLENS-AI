from typing import Optional, ClassVar
from datetime import datetime
from sqlmodel import SQLModel, Field

class Article(SQLModel, table=True):
    __tablename__: ClassVar[str] = "articles"  # pyright: ignore[reportAssignmentType]

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    content: Optional[str] = None
    link: str = Field(unique=True)
    source: str = Field(index=True)

    is_processed: bool = Field(default=False)
    is_embedded: bool = Field(default=False)

    published_at: datetime = Field(default_factory=datetime.utcnow)