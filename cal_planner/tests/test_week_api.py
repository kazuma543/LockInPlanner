import pytest 
from datetime import date
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from cal_planner.models import Week, Task, PlannedBlock, ActualLog
from django.urls import reverse
from cal_planner.services import calculate_actual_time_amount,calculate_planned_time_amount,calculate_achievement_percentage

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
#Plannedblock Test
'''@pytest.fixture
def alice_task(db):
    alice = User.objects.create_user("alice", password="x")
    week = Week.objects.create(user=alice, start_date=date(2026, 11, 9))
    return Task.objects.create(week=week, name="Coding", target_minutes="1200")

@pytest.mark.django_db
def test_block_requires_login(client):
    res = client.get(reverse("plannedblock-list"))
    assert res.status_code in (401, 403)

@pytest.mark.django_db
def test_can_create_block_in_own_task(client, alice_task):
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
'''
#Overlapping test
'''def make_block(task, start, end):
    return PlannedBlock.objects.create(task=task, start_time=start, end_time=end)

@pytest.mark.django_db
def test_overlapping_block_rejected(client, alice_task):
    make_block(alice_task, "2026-11-09T07:00:00+11:00", "2026-11-09T09:00:00+11:00")
    client.force_authenticate(alice_task.week.user)
    res = client.post(reverse("planned-block-list"), {
        "task": alice_task.id,
        "start_time": "2026-11-09T08:00:00+11:00",
        "end_time": "2026-11-09T10:00:00+11:00",
    })
    assert res.status_code == 400

@pytest.mark.django_db
def test_touching_blocks_allowed(client, alice_task):
    make_block(alice_task, "2026-11-09T07:00:00+11:00", "2026-11-09T09:00:00+11:00")
    client.force_authenticate(alice_task.week.user)
    res = client.post(reverse("planned-block-list"), {
        "task": alice_task.id,
        "start_time": "2026-11-09T09:00:00+11:00",
        "end_time": "2026-11-09T10:00:00+11:00",
    })
    assert res.status_code == 201

@pytest.mark.django_db
def test_other_users_blocks_do_not_conflict(client, alice_task):
    make_block(alice_task, "2026-11-09T07:00:00+11:00", "2026-11-09T09:00:00+11:00")
    bob = User.objects.create_user("bob", password="x")
    bob_week = Week.objects.create(user=bob, start_date=date(2026, 11, 9))
    bob_task = Task.objects.create(week=bob_week, name="Coding", target_minutes=60)
    client.force_authenticate(bob)
    res = client.post(reverse("planned-block-list"), {
        "task": bob_task.id,
        "start_time": "2026-11-09T07:00:00+11:00",
        "end_time": "2026-11-09T09:00:00+11:00",
    })
    assert res.status_code == 201

@pytest.mark.django_db
def test_can_update_own_block_without_self_conflict(client, alice_task):
    block = make_block(alice_task, "2026-11-09T07:00:00+11:00", "2026-11-09T09:00:00+11:00")
    client.force_authenticate(alice_task.week.user)
    res = client.patch(reverse("planned-block-detail", args=[block.id]),
                       {"end_time": "2026-11-09T09:30:00+11:00"})
    assert res.status_code == 200'''

#Actual Log test
'''@pytest.fixture
def alice_task(db):
    alice = User.objects.create_user("alice", password="x")
    week = Week.objects.create(user=alice, start_date=date(2026, 11, 9))
    return Task.objects.create(week=week, name="Coding", target_minutes=1200)

@pytest.mark.django_db
def test_log_requires_login(client):
    res = client.get(reverse("actuallog-list"))
    assert res.status_code in (401, 403)

@pytest.mark.django_db
def test_can_create_log_in_own_task(client, alice_task):
    client.force_authenticate(alice_task.week.user)
    res = client.post(reverse("actuallog-list"),
                        {"task":alice_task.id, "start_time":"2026-11-09T07:00:00+11:00", "end_time":"2026-11-09T09:00:00+11:00","note":"Tough","focus":"3"})
    assert res.status_code == 201

@pytest.mark.django_db
def test_end_must_be_after_start(client, alice_task):
    client.force_authenticate(alice_task.week.user)
    res = client.post(reverse("actuallog-list"), {
        "task": alice_task.id,
        "start_time": "2026-11-09T09:00:00+11:00",
        "end_time": "2026-11-09T07:00:00+11:00",
        "note":"Tough",
        "focus":"3"
    })

    assert res.status_code  == 400

@pytest.mark.django_db
def test_cannot_use_other_users_task(client, alice_task):
    bob = User.objects.create_user("bob", password="x")
    res_client = client
    res_client.force_authenticate(bob)
    res = res_client.post(reverse("actuallog-list"), {
        "task": alice_task.id,
        "start_time": "2026-11-09T07:00:00+11:00",
        "end_time": "2026-11-09T09:00:00+11:00",
        "note":"Tough",
        "focus":"3"
    })
    assert res.status_code == 400

@pytest.mark.django_db
def test_user_only_sees_own_tasks(client, alice_task):
    bob = User.objects.create_user("bob",password="y")
    week = Week.objects.create(user=bob, start_date=date(2026, 11, 9))
    bob_task = Task.objects.create(week=week, name="Coding", target_minutes=1200)
    ActualLog.objects.create(task=alice_task, start_time="2026-11-09T09:00:00+11:00", end_time= "2026-11-09T09:00:00+11:00",
        note="Tough",
        focus="3")
    ActualLog.objects.create(task=bob_task, start_time="2026-11-10T09:00:00+11:00", end_time= "2026-11-11T09:00:00+11:00",
        note="Easy",
        focus="5")

    client.force_authenticate(alice_task.week.user)
    res = client.get(reverse("actuallog-list"))

    assert len(res.json()) == 1

@pytest.mark.django_db
def test_focus_score_must_be_less_than_5(client, alice_task):
    client.force_authenticate(alice_task.week.user)
    res = client.post(reverse("actuallog-list"), {
        "task": alice_task.id,
        "start_time": "2026-11-09T07:00:00+11:00",
        "end_time": "2026-11-09T09:00:00+11:00",
        "note":"Tough",
        "focus":"8"
    })

    assert res.status_code  == 400'''

#Weekly report test
@pytest.fixture
def alice_task(db):
    alice = User.objects.create_user("alice", password="x")
    week = Week.objects.create(user=alice, start_date=date(2026, 11, 9))
    return Task.objects.create(week=week, name="Coding", target_minutes=1200)

@pytest.mark.django_db
def test_report_does_not_mix_other_users(client, alice_task):
    bob = User.objects.create_user("bob",password="y")
    bob_week = Week.objects.create(user=bob, start_date=date(2026, 11, 9))
    bob_task = Task.objects.create( week=bob_week, name="Coding", target_minutes=1200)
    ActualLog.objects.create(task=alice_task, start_time="2026-11-09T09:00:00+11:00", end_time= "2026-11-09T10:00:00+11:00",
        note="Tough",
        focus="3")
    ActualLog.objects.create(task=bob_task, start_time="2026-11-10T09:00:00+11:00", end_time= "2026-11-11T09:00:00+11:00",
        note="Easy",
        focus="5")

    client.force_authenticate(alice_task.week.user)
    res = client.get(reverse("week-get-achievement-percentage",args=[alice_task.week.id]))

    assert res.status_code == 200
    task_ids = [item["task_id"] for item in res.json()]
    assert alice_task.id in task_ids
    assert bob_task.id not in task_ids

@pytest.mark.django_db
def test_cannot_view_other_user_report(client, alice_task):
    bob = User.objects.create_user("bob", password="y")

    client.force_authenticate(bob)
    res = client.get(
        reverse("week-get-achievement-percentage", args=[alice_task.week.id])
    )   

    assert res.status_code == 404

@pytest.mark.django_db
def test_report_does_not_mix_other_task_from_same_user(client, alice_task):
    week_2 = Week.objects.create(user=alice_task.week.user, start_date=date(2026, 11,16))
    other_week_task = Task.objects.create(week=week_2, name="Writing", target_minutes = 300)
    ActualLog.objects.create(task=other_week_task, start_time="2026-11-16T09:00:00+11:00", end_time= "2026-11-18T09:00:00+11:00",
        note="Tough",
        focus="3")
    ActualLog.objects.create(task=alice_task, start_time="2026-11-09T09:00:00+11:00", end_time= "2026-11-10T09:00:00+11:00",
        note="Tough",
        focus="3")
    client.force_authenticate(alice_task.week.user)
    res = client.get(reverse("week-get-achievement-percentage", 
                        args=[alice_task.week.id]))
    assert res.status_code == 200
    task_ids = [item["task_id"] for item in res.json()]
    assert alice_task.id in task_ids
    assert other_week_task.id not in task_ids

