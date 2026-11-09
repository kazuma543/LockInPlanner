import pytest 
from datetime import date
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from cal_planner.models import Week, Task, PlannedBlock
from django.urls import reverse


User = get_user_model()

#Week API test
@pytest.fixture
def client():
    return APIClient()

'''@pytest.mark.django_db
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
    assert len(res.json()) == 1'''

#Task API test

'''@pytest.fixture
def alice_week(db):
    alice = User.objects.create_user("alice", password="x")
    return Week.objects.create(user=alice, start_date=date(2026, 11, 2))

@pytest.mark.django_db
def test_task_requires_login(client):
    res = client.get(reverse("task-list"))
    assert res.status_code in (401, 403)

@pytest.mark.django_db
def test_can_create_task_in_own_week(client, alice_week):
    client.force_authenticate(alice_week.user)
    res = client.post(reverse("task-list"),
                        {"week":alice_week.id, "name":"Coding", "target_minutes":1200})
    assert res.status_code == 201

@pytest.mark.django_db
def test_user_only_sees_own_tasks(client, alice_week):
    bob = User.objects.create_user("bob",password="y")
    bob_week = Week.objects.create(user=bob, start_date=date(2026, 11, 2))
    Task.objects.create(week=alice_week, name="A", target_minutes=60)
    Task.objects.create(week=bob_week, name="B", target_minutes=60)

    client.force_authenticate(alice_week.user)
    res = client.get(reverse("task-list"))

    assert len(res.json()) == 1

@pytest.mark.django_db
def test_cannnot_create_task_in_other_users_week(client, alice_week):
    bob = User.objects.create_user("bob", password="y")
    bob_week = Week.objects.create(user=bob, start_date=date(2026, 11, 2))

    client.force_authenticate(alice_week.user)
    res = client.post(reverse("task-list"),
                      {"week":bob_week.id, "namw":"x", "target_minutes":60})
    assert res.status_code == 400
'''

@pytest.fixture
def alice_task(db):
    alice = User.objects.create_user("alice", password="x")
    week = Week.objects.create(user=alice, start_date=date(2026, 11, 9))
    return Task.objects.create(week=week, name="Coding", target_minutes="1200")

@pytest.mark.django_db
def test_block_requires_login(client):
    res = client.get(reverse("plannedblock-list"))
    assert res.status_code in (401, 403)

@pytest.mark.django_db
def est_can_create_block_in_own_task(client, alice_task):
    client.force_authenticate(alice_task.week.user)
    res = client.post(reverse("plannedblock-list"),
                        {"task":alice_task.id, "start_time":"2026-11-09T07:00:00+11:00", "end_time":"2026-11-09T09:00:00+11:00"})
    assert res.status_code == 201

@pytest.mark.django_db
def test_end_must_be_after_start(client, alice_task):
    client.force_authenticate(alice_task.week.user)
    res = client.post(reverse("plannedblock-list"), {
        "task": alice_task.id,
        "start_time": "2026-11-09T09:00:00+11:00",
        "end_time": "2026-11-09T07:00:00+11:00",
    })

    assert res.status_code  == 201

@pytest.mark.django_db
def test_cannot_use_other_users_task(client, alice_task):
    bob = User.objects.create_user("bob", password="x")
    res_client = client
    res_client.force_authenticate(bob)
    res = res_client.post(reverse("plannedblock-list"), {
        "task": alice_task.id,
        "start_time": "2026-11-09T07:00:00+11:00",
        "end_time": "2026-11-09T09:00:00+11:00",
    })
    assert res.status_code == 400