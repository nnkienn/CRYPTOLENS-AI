Day 1:

Sequential
→ chạy tuần tự từng task

Concurrent (async + gather)
→ chạy nhiều task bất đồng bộ cùng lúc

async
→ khai báo coroutine

await
→ trong lúc chờ I/O thì event loop chạy task khác

FastAPI xử lý nhiều request cùng lúc vì:

ASGI server tạo coroutine cho mỗi request
event loop chạy các coroutine concurrently

asyncio.gather chỉ dùng để chạy nhiều task
bên trong một request
tại sao FastAPI vẫn xử lý 1000 request cùng lúc ?? FastAPI tự concurrent giữa các request
gather concurrent bên trong một request

1. Concurrency của Server (FastAPI + ASGI)
Đây là "Bên ngoài nhìn vào".

Cơ chế: Khi 100 người dùng cùng truy cập vào website của ông, ASGI Server (như Uvicorn) sẽ tạo ra 100 cái Coroutines.

Event Loop sẽ đảo qua đảo lại giữa 100 người này. Nếu người số 1 đang đợi database trả kết quả, nó nhảy sang phục vụ người số 2 ngay lập tức.

Kết luận: FastAPI lo việc "tiếp khách" đông cùng lúc mà không cần ông phải làm gì thêm.

2. Concurrency của Logic (asyncio.gather)
Đây là "Bên trong nhìn ra".

Cơ chế: Giả sử người dùng số 1 gọi API /get-dashboard. Để có dữ liệu dashboard, ông cần:

Lấy giá BTC từ Binance.

Lấy tin tức từ Postgres.

Lấy thông báo từ Redis.

Nếu ông viết await tuần tự cho từng cái, người dùng sẽ phải đợi: Thời gian (1 + 2 + 3).

Nếu ông dùng asyncio.gather(1, 2, 3), người dùng chỉ phải đợi bằng: Thời gian của cái lâu nhất.

Kết luận: gather dùng để tối ưu tốc độ cho MỘT request cụ thể cần làm nhiều việc I/O cùng lúc.