# [Project Name / App Name]

A calendar app with a task list and a log page to track the original plan and record progress compared with the plan.

## 1. Background & Purpose (Why I Built It)
*   **The Problem:** When I was a student, I always struggled to manage time for study, workouts, a part-time job, and social activities. Existing calendar apps are just planners with a simple to-do list function.
*   **The Approach:** Make a plan in the same way as a usual calendar app, then the app calculates how much time you will spend on one task. At the end of the day, users need to record the actual time spent and what they have done. After all, the app will return the result weekly.
*   **Target User:** Mostly uni students.

## 2. Core Features (What It Does)
*   [ ] **Core Feature A:** Making a weekly plan and listing tasks for the week.
*   [ ] **Core Feature B:** Recording what they have done and how long it took.
*   [ ] **Key Selling Point C (Differentiation):** Setting how much time they want to spend on each task and generating a report that compares the plan and the result.

## 3. Tech Stack & Rationale

*   **Language:** Python 3.14
*   **Framework:** Django 5.2 LTS. It includes the ORM, authentication and an admin site, so I can focus on the business logic.
*   **API:** Django REST Framework + drf-spectacular. DRF is the standard way to build REST APIs in Django, serializers handle validation, and Swagger docs are generated automatically.
*   **Database:** PostgreSQL (via Docker). It is closer to production than SQLite, and the same database runs locally and in CI.
*   **Testing:** pytest + pytest-django, covering the business rules (time budget limit, overlapping blocks, weekly report).
*   **CI:** GitHub Actions, running lint (ruff) and tests on every push.
*   **UI (planned):** Django templates + Bootstrap, added after the API is complete.
*   **Other libraries:** psycopg (PostgreSQL driver), python-dotenv (environment variables), gunicorn (production server in Docker).

## 4. Architecture & Directory Structure

```text
CLDA/
├── manage.py
├── config/                 # Project settings and root URLs
├── planner/                # Main app
│   ├── models.py           # Week, Task, PlannedBlock, ActualLog
│   ├── serializers.py      # Validation and API representation
│   ├── views.py            # API endpoints
│   ├── services.py         # Business rules (budget check, overlap check, weekly report)
│   └── tests/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── .github/workflows/ci.yml
└── README.md
```

**Design notes**
*   Business rules live in `services.py`, separate from the views, so they can be unit-tested without HTTP.
*   Views stay thin: validate input, call a service, return the response.

## 5. Technical Challenges & Key Learnings (Interview Talking Points)
Keep a running log of blockers you encountered and how you systematically resolved them (update this dynamically as you build).

*   **The Issue:** [e.g., "The UI would freeze and lag whenever a web scraping task was triggered."]
*   **The Root Cause:** [e.g., "The network request was running on the main UI thread, blocking user interactions."]
*   **The Solution:** [e.g., "Implemented Python's `threading` module to offload network operations to a background thread, keeping the UI completely responsive."]

## 6. Setup & Installation (Mac Guide)
Ensures recruiters or developers looking at your GitHub repository can spin up and test your application locally in under 3 minutes.

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
