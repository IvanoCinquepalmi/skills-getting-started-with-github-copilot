import copy
import pytest
from fastapi.testclient import TestClient

from src.app import app, activities

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_activities():
    """Reset the in-memory activities before/after each test"""
    orig = copy.deepcopy(activities)
    yield
    activities.clear()
    activities.update(orig)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert "Tennis Club" in data


def test_signup_success():
    email = "newstudent@mergington.edu"
    resp = client.post(f"/activities/Programming%20Class/signup?email={email}")
    assert resp.status_code == 200
    assert resp.json()["message"] == f"Signed up {email} for Programming Class"
    assert email in activities["Programming Class"]["participants"]


def test_signup_duplicate():
    email = "emma@mergington.edu"  # already in Programming Class from seed data
    resp = client.post(f"/activities/Programming%20Class/signup?email={email}")
    assert resp.status_code == 400


def test_signup_nonexistent_activity():
    resp = client.post("/activities/Nonexistent/signup?email=foo@bar.com")
    assert resp.status_code == 404


def test_unregister_success():
    # alex@mergington.edu is registered for Tennis Club in seed data
    email = "alex@mergington.edu"
    resp = client.delete(f"/activities/Tennis%20Club/unregister?email={email}")
    assert resp.status_code == 200
    assert resp.json()["message"] == f"Unregistered {email} from Tennis Club"
    assert email not in activities["Tennis Club"]["participants"]


def test_unregister_nonexistent_activity():
    resp = client.delete("/activities/NoActivity/unregister?email=someone@x.com")
    assert resp.status_code == 404


def test_unregister_nonexistent_participant():
    resp = client.delete("/activities/Tennis%20Club/unregister?email=notregistered@x.com")
    assert resp.status_code == 400
