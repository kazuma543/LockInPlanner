# [LockInPlanner]

A calendar app with a task list and a log page to track the original plan and record progress compared with the plan.

## 1. Background & Purpose (Why I Built It)
*   **The Problem:** When I was a student, I always struggled to manage time for study, workouts, a part-time job, and social activities. Existing calendar apps are just planners with a simple to-do list function.
*   **The Approach:** Users plan their week as in a regular calendar app, and the app calculates the planned time for each task At the end of the day, users need to record the actual time spent and what they have done. Finally, the app generates a weekly report comparing plan and actual.
*   **Target User:** Mostly uni students.

## 2. Core Features (What It Does)
*    **Weekly planning:** Making a weekly plan and listing tasks for the week.
*    **Actual time logging:** Recording what they have done and how long it took.
*    **Plan vs. actual report:** Setting how much time they want to spend on each task and generating a report that compares the plan and the result.

## 3. Tech Stack & Rationale

*   **Language:** Python 3.13
*   **Framework:** Django 5.2 LTS. It includes the ORM, authentication and an admin site, so I can focus on the business logic.
*   **API:** Django REST Framework + drf-spectacular. DRF is the standard way to build REST APIs in Django, serializers handle validation, and Swagger docs are generated automatically.
*   **Database:** PostgreSQL (via Docker). It is closer to production than SQLite, and the same database runs locally and in CI.
*   **Testing:** pytest + pytest-django, covering the business rules (overlapping blocks, weekly report).
*   **CI:** GitHub Actions, running lint (ruff) and tests on every push.
![CI](https://github.com/kazuma543/LockInPlanner/actions/workflows/ci.yml/badge.svg)
*   **UI (planned):** Django templates + Bootstrap, added after the API is complete.
*   **Other libraries:** psycopg (PostgreSQL driver), python-dotenv (environment variables).

## 4. Architecture & Directory Structure

```text
CLDA/
├── manage.py
├── cl_project/                 # Project settings and root URLs
├── cal_planner/                # Main app
│   ├── admin.py
│   ├── apps.py
│   ├── models.py           # Week, Task, PlannedBlock, ActualLog
│   ├── serializers.py      # Validation and API representation
│   ├── views.py            # API endpoints
│   ├── services.py         # Business rules (overlap check, weekly report)
│   ├── urls.py
│   └── tests/
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── .github/workflows/ci.yml
├── ruff.toml
└── README.md

```

**Design notes**
*   Business rules live in `services.py`, separate from the views, so they can be unit-tested without HTTP.
*   Views stay thin: validate input, call a service, return the response.

## 5. Technical Challenges & Key Learnings 
There were several technical challenges while developing this app. Here are the ones that taught me the most.

1
*   **The Issue:** Some tests passed even though invalid data was being accepted.
*   **The Root Cause:** One test asserted a 201 response for invalid input, so it confirmed the bug instead of catching it. Another was never collected because its name did not start with `test_`.
*   **The Solution:** I deliberately broke the code (for example, `__lt` to `__lte`) to confirm that each test fails when it should.

2
*   **The Issue:** The weekly report contained a mix of data for all users and all weeks.
*   **The Root Cause:**  The calculation code did not use the given week data.
*   **The Solution:** After reproducing the bug with a failing test, I filtered the queries with task__week=week.

3
*   **The Issue:** There was a risk that data could be created in other people’s Weeks or Tasks. 
*   **The Root Cause:** The foreign key options covered all users.
*   **The Solution:** Filtered the key using 'get_fields()' in serialiser.

4
*   **The Issue:** The API raised an error: "expected a `date`, but got a `datetime`".
*   **The Root Cause:** The migration history still defined `start_date` as a `DateTimeField`, while the model had been changed to `DateField`, so the database column and the model were out of sync.
*   **The Solution:** I created a migration to alter the column to `DateField`.

5
*   **The Issue:** CI crushed twice when it's deployed.
*   **The Root Cause:** Miss 'S' in 'POSTGRES'.
*   **The Solution:** I read the first failing line in each log to find the cause, and fixed the workflow file.


## 6. Setup & Installation (Mac)

Requires Python 3.13 and Docker Desktop.

```bash
git clone https://github.com/kazuma543/LockInPlanner.git
cd LockInPlanner

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env        # then set DB_PASS in .env
docker compose up -d db     # PostgreSQL in Docker
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver  # API docs: http://127.0.0.1:8000/api/docs/
```

Run the tests:

## 7. Future Work
time budget limit,

```bash
# Clone the repository
git clone [YOUR_REPOSITORY_URL]
cd [PROJECT_DIRECTORY_NAME]

# Create and activate the virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python3 src/main.py
```
