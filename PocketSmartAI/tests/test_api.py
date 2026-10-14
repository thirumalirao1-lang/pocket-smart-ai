import os
os.environ["USE_MOCK_AI"] = "true"

from app import app

def test_health():
    client = app.test_client()
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json["success"] is True

def test_home():
    client = app.test_client()
    response = client.post("/api/generate-home", json={
        "budget": 100000,
        "rooms": [{"name": "Living Room", "items": ["sofa", "TV unit"]}]
    })
    assert response.status_code == 200
    assert response.json["success"] is True

def test_party():
    client = app.test_client()
    response = client.post("/api/generate-party", json={
        "budget": 50000, "guests": 40,
        "event_type": "Birthday", "venue": "Chennai Hall"
    })
    assert response.status_code == 200
    assert response.json["success"] is True

def test_jewelry():
    client = app.test_client()
    response = client.post("/api/generate-jewelry", data={
        "budget": "30000", "occasion": "Wedding", "style": "Traditional"
    })
    assert response.status_code == 200
    assert response.json["success"] is True
