# Test file for NOA API endpoints
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data


def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data


def test_webhook_invalid_json():
    """Test webhook with invalid JSON"""
    response = client.post("/api/v1/webhook", json={"invalid": "data"})
    assert response.status_code == 400


def test_webhook_invalid_event():
    """Test webhook with invalid event type"""
    response = client.post(
        "/api/v1/webhook", json={"event": "invalid_event", "data": {}}
    )
    assert response.status_code == 400


def test_webhook_from_me():
    """Test webhook with message from self"""
    response = client.post(
        "/api/v1/webhook",
        json={
            "event": "messages.upsert",
            "data": {
                "key": {
                    "remoteJid": "1234567890@s.whatsapp.net",
                    "fromMe": True,
                    "id": "test_message_id",
                },
                "message": {"conversation": "test message"},
            },
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ignored_from_me"


def test_webhook_invalid_phone():
    """Test webhook with invalid phone number"""
    response = client.post(
        "/api/v1/webhook",
        json={
            "event": "messages.upsert",
            "data": {
                "key": {
                    "remoteJid": "invalid_phone",
                    "fromMe": False,
                    "id": "test_message_id",
                },
                "message": {"conversation": "test message"},
            },
        },
    )
    assert response.status_code == 400


def test_webhook_no_text():
    """Test webhook with no text content"""
    response = client.post(
        "/api/v1/webhook",
        json={
            "event": "messages.upsert",
            "data": {
                "key": {
                    "remoteJid": "1234567890@s.whatsapp.net",
                    "fromMe": False,
                    "id": "test_message_id",
                },
                "message": {},
            },
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "no_text"


def test_webhook_valid_message():
    """Test webhook with valid message"""
    response = client.post(
        "/api/v1/webhook",
        json={
            "event": "messages.upsert",
            "data": {
                "key": {
                    "remoteJid": "1234567890@s.whatsapp.net",
                    "fromMe": False,
                    "id": "test_message_id",
                },
                "message": {"conversation": "Hola, quiero información"},
            },
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "accepted"
    assert data["phone"] == "1234567890"
