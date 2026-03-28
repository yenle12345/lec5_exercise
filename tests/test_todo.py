import pytest
from fastapi.testclient import TestClient
from app.main import app  # Sửa lại đường dẫn import cho đúng cấu trúc của bạn
from app.dependencies.auth import get_current_user
from datetime import datetime

client = TestClient(app)

# Mock user data
class MockUser:
    def __init__(self, id):
        self.id = id

# Helper: Mock dependency (Dùng để giả lập người dùng đã đăng nhập)
async def mock_get_current_user():
    return MockUser(id=1)

# --- TESTS ---

# 1. Test tạo thành công
def test_create_todo_success():
    # Override để bỏ qua bước check JWT thật
    app.dependency_overrides[get_current_user] = mock_get_current_user
    
    payload = {
        "id": 1,
        "title": "Học Pytest nâng cao", 
        "is_done": False,
        "due_date": datetime.now().isoformat(),
        "tags": ["python", "test"]
    }
    
    response = client.post("/api/v1/todos/todos", json=payload)
    app.dependency_overrides.clear()
    
    # Nếu API của bạn trả về 201 Created thì sửa thành 201
    assert response.status_code == 200 
    assert response.json()["title"] == payload["title"]

# 2. Test Validation Fail (Dữ liệu gửi lên sai định dạng)
def test_create_todo_validation_fail():
    app.dependency_overrides[get_current_user] = mock_get_current_user
    
    # Gửi title là một list (sai kiểu string) để ép nó lỗi 422
    payload = {"title": ["Đây không phải string"], "tags": []}
    
    response = client.post("/api/v1/todos/todos", json=payload)
    app.dependency_overrides.clear()
    
    # Chỗ này PHẢI là 422 mới đúng logic test validation
    assert response.status_code == 422

# 3. Test 404 Not Found (Lấy Todo không tồn tại)
def test_get_todo_not_found():
    response = client.get("/api/v1/todos/todos/999999") 
    assert response.status_code == 404

# 4. Test Auth Fail (Chưa đăng nhập)
def test_create_todo_auth_fail():
    # Không override get_current_user -> Mặc định sẽ lỗi Auth
    payload = {"title": "No Auth", "tags": []}
    response = client.post("/api/v1/todos/todos", json=payload)
    
    # FastAPI/Starlette mặc định trả 401 hoặc 403 nếu thiếu Token
    assert response.status_code in [401, 403]