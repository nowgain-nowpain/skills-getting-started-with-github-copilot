from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert "Chess Club" in data
    assert isinstance(data["Chess Club"]["participants"], list)


def test_signup_and_unregister_flow():
    activity = "Chess Club"
    email = "pytest_tester@example.com"

    # Ensure the test email is not currently signed up
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    if email in data[activity]["participants"]:
        # If present (from previous failed cleanup), remove first
        client.delete(f"/activities/{activity}/unregister", params={"email": email})

    # Sign up
    signup = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert signup.status_code == 200
    assert "Signed up" in signup.json().get("message", "")

    # Verify participant appears in activity
    resp = client.get("/activities")
    data = resp.json()
    assert email in data[activity]["participants"]

    # Unregister
    unreg = client.delete(f"/activities/{activity}/unregister", params={"email": email})
    assert unreg.status_code == 200
    assert "Unregistered" in unreg.json().get("message", "")

    # Verify participant removed
    resp = client.get("/activities")
    data = resp.json()
    assert email not in data[activity]["participants"]
