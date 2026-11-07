import pytest 
from datetime import date
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from cal_planner.models import Week 

User = get_user_model()

@pytest.fixture
def client():
    return APIClient()

@pytest.mark.django_db
def test_request_login(client):
    res = client.get("/api/v1/weeks/")
    assert res.status_code in (401, 403)

@pytest.mark.django_db
def test_user_only_sees_own_weeks(client):
    alice = User.objects.create_user("alice", password="x")
    bob = User.objects.create_user("bob", password="y")
    Week.objects.create(user=alice, start_date=date(2026, 11,7))
    Week.objects.create(user=bob, start_date=date(2026, 11, 7))

    client.force_authenticate(alice)
    res = client.get("/api/v1/weeks/")

    assert res.status_code == 200
    assert len(res.json()) == 1