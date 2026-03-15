from app.schemas.article import Article
from datetime import datetime
from pydantic import ValidationError

# 1. Dữ liệu "siêu bẩn" mô phỏng từ RSS
raw_data = {
    "title": "   BITCOIN IS PUMPING!!!   ", # Thừa khoảng trắng
    "content": "Some crypto news content...",
    "source": "https://coindesk.com",
    "published_at": "2026-03-15T23:47:00",    # String ngày tháng
    "asset_symbols": ["btc", "  btc  ", "eth", ""] # Trùng, thừa cách, có rỗng
}

print("--- BẮT ĐẦU TEST SCHEMA ---")

try:
    # Đổ dữ liệu vào phễu Article
    article = Article(**raw_data)

    # Kiểm tra kết quả
    print(f"✅ Title (đã trim): '{article.title}'")
    print(f"✅ Symbols (đã dọn): {article.asset_symbols}")
    print(f"✅ Date (đã parse): {type(article.published_at)} - {article.published_at}")
    
    # Thử sửa dữ liệu (vì ta đặt frozen=True)
    # article.title = "New Title" # Nếu bỏ comment dòng này sẽ lỗi
    
except ValidationError as e:
    print("❌ Dữ liệu không hợp lệ!")
    print(e.json())