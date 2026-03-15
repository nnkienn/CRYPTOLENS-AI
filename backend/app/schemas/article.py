from pydantic import BaseModel, Field , ConfigDict, field_validator
from datetime import datetime
from typing import Optional, List
import re

class Article(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace= True, # loại bỏ khoảng trắng 
        from_attributes= True, # cho phép sử dụng tên trường khác với tên biến trong class
        frozen = True # làm cho đối tượng bất biến không bị sửa (immutable)
    )

    title : str = Field(..., min_length= 5, max_length= 100, description="Tiêu đề của bài viết")
    content : str = Field(..., min_length= 20, description="Nội dung của bài viết")
    source : str = Field (..., min_length= 5, max_length= 100, description="Nguồn của bài viết")
    published_at : Optional[datetime] = Field(None, description="Ngày xuất bản của bài viết")
    asset_symbols : List[str] = Field(..., description="Danh sách các mã coin liên quan đến bài viết")


    @field_validator('asset_symbols')
    @classmethod
    def clean_symbols(cls, v : List[str]) -> List[str]:
        return list(set(s.upper().strip() for s in v if s))    
    
    @field_validator('published_at', mode='before')
    @classmethod
    def parse_datetime(cls, v):
        return v

