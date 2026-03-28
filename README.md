# Todo API Project

Hệ thống quản lý công việc (Todo) xây dựng bằng FastAPI, SQLAlchemy và PostgreSQL.

## Cấu trúc dự án
- `repositories/`: Thao tác trực tiếp với Database.
- `services/`: Xử lý logic nghiệp vụ (Business Logic).
- `routers/`: Định nghĩa các API endpoints.
- `tests/`: Chứa các kịch bản kiểm thử với Pytest.

## Cách khởi chạy

### 1. Sử dụng Docker (Nhanh nhất)
Yêu cầu: Đã cài Docker.
```bash
docker-compose up --build