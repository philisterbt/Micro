from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_register_and_login():
    # Register
    reg_response = client.post("/register", json={"username": "testuser", "password": "testpassword"})
    assert reg_response.status_code == 200
    
    # Login
    login_response = client.post("/login", data={"username": "testuser", "password": "testpassword"})
    assert login_response.status_code == 200
    assert "access_token" in login_response.json()

def test_verify_invalid_token():
    response = client.get("/verify?token=invalidtoken")
    assert response.status_code == 401
