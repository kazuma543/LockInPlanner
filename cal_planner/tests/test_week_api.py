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
    res = client.get("/api/v1/weeks")
    assert res.status_code in (401, 403)

@pytest.mark.django_db
    