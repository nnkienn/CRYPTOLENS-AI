from typing import Optional, ClassVar
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Boolean
from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):
    __tablename__: ClassVar[str] = "users"  # pyright: ignore[reportAssignmentType]

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(
        sa_column=Column(String, unique=True, index=True, nullable=False)
    )
    hashed_password: str = Field(sa_column=Column(String, nullable=False))
    is_active: bool = Field(sa_column=Column(Boolean, nullable=False, default=True))
    is_pro: bool = Field(sa_column=Column(Boolean, nullable=False, default=False))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(
        sa_column=Column(DateTime, nullable=True, onupdate=datetime.utcnow)
    )