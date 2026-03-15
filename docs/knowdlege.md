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

📝 Tổng kết Day 4 - Pydantic Data Models
Xử lý chuỗi (String manipulation):

.upper(): IN HOA TOÀN BỘ.

.strip(): Dọn dẹp khoảng trắng dư thừa ở hai đầu.

Xử lý danh sách (Collection logic):

set(...): Cái phễu lọc trùng (giống HashSet). Trong Python, set chỉ chứa các phần tử duy nhất.

list(...): Ép kiểu ngược lại về danh sách (giống ArrayList) để giữ đúng định dạng dữ liệu trả về.

Pydantic Core:

@field_validator: "Người gác cổng" cho từng trường dữ liệu. Bạn muốn nắn dòng nào thì gọi tên dòng đó ra để xử lý.

frozen=True: Khóa object lại. Một khi đã tạo ra bài báo là "bất di bất dịch", không ai sửa lung tung được nữa.

from_attributes=True: Chiếc vé thông hành để Schema này làm việc được với Database (SQLAlchemy) vào ngày mai.

💡 Một mẹo nhỏ cho bạn (Tips)
Trong Python, khi bạn thấy cụm [s.upper().strip() for s in v if s], hãy nhớ nó là một bộ lọc 3 trong 1: Duyệt -> Lọc -> Biến đổi.

Day 4 coi như "Done"! Bạn đã có:

Cấu trúc thư mục chuẩn.

Schema bảo mật dữ liệu.

Cách test module với python -m.