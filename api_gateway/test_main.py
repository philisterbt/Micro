from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200

@patch("main.requests.request")
def test_proxy_auth(mock_request):
    # Mock upstream response
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {"status": "ok"}
    mock_request.return_value = mock_resp

    response = client.get("/auth/health")
    assert response.status_code == 200
