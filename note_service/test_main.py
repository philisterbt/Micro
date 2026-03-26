from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200

@patch("main.requests.get")
@patch("main.pika.BlockingConnection")
def test_create_note(mock_pika, mock_requests_get):
    # Mock auth verification
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {"username": "testuser"}
    mock_requests_get.return_value = mock_resp
    
    # Mock rabbitmq
    mock_conn = MagicMock()
    mock_channel = MagicMock()
    mock_conn.channel.return_value = mock_channel
    mock_pika.return_value = mock_conn

    response = client.post(
        "/notes",
        json={"title": "Test Note", "content": "This is a test note."},
        headers={"Authorization": "Bearer fake_token"}
    )
    
    assert response.status_code == 200
    assert response.json()["message"] == "Note created"
    assert response.json()["note"]["title"] == "Test Note"
