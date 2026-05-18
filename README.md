# Task Management API

A scalable Task Management API built with Django and Django REST Framework (DRF). The project supports task management operations with asynchronous task processing using Celery and is containerized with Docker for production deployment on AWS.

---

## Features

- User registration and authentication
- JWT authentication
- Task CRUD operations
- Task filtering and search
- Background task processing using Celery
- Email notifications
- Dockerized application
- CI/CD with GitHub Actions
- API testing with Pytest
- Production-ready deployment setup

---

## Tech Stack

### Backend
- Python
- Django
- Django REST Framework

### Database
- SQLite (Development)
- PostgreSQL (Production)

### Background Tasks
- Celery
- RabbitMQ

### DevOps

- Docker
- Docker Compose
- GitHub Actions
- AWS ECS
- AWS RDS
- Nginx

### Testing & Quality

- Pytest
- Ruff
- Pre-commit hooks
- Bandit

---

## Project Structure

```bash
Task-Management/
│
├── .github/                 # GitHub Actions workflow
├── accounts/                # Authentication app
├── app/                     # Main task management app
├── core/                    # Project settings
├── media/                   # Uploaded files
├── reports/                 # Generated reports
├── static/                  # Static files
├── templates/               # HTML templates
│
├── .dockerignore
├── .env
├── .gitignore
├── .pre-commit-config.yaml
├── conftest.py
├── docker-compose.yml
├── Dockerfile
├── manage.py
├── pyproject.toml
├── pytest.ini
├── requirements.txt
└── README.md
```

---

## Local Setup

Clone repository:

```bash
git clone https://github.com/your-username/Task-Management.git

cd Task-Management
```

Create virtual environment:

```bash
python -m venv venv
```

Activate environment:

Linux/Mac:

```bash
source venv/bin/activate
```

Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create `.env` file:

```env
SECRET_KEY=your_secret_key

DEBUG=True

DB_NAME=task_db
DB_USER=postgres
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432

CELERY_BROKER_URL=amqp://guest:guest@rabbitmq:5672//

EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=example@gmail.com
EMAIL_HOST_PASSWORD=password
EMAIL_USE_TLS=True
```

---

## Database Setup

Apply migrations:

```bash
python manage.py makemigrations

python manage.py migrate
```

Create admin user:

```bash
python manage.py createsuperuser
```

---

## Run Application

Start Django server:

```bash
python manage.py runserver
```

Application:

```bash
http://127.0.0.1:8000/
```

---

## Run Celery Worker

```bash
celery -A core worker -l info
```

Run Celery Beat:

```bash
celery -A core beat -l info
```

---

## Docker Setup

Build containers:

```bash
docker-compose build
```

Run application:

```bash
docker-compose up
```

Run in background:

```bash
docker-compose up -d
```

Stop containers:

```bash
docker-compose down
```

---

## Testing

Run tests:

```bash
pytest
```

Generate coverage:

```bash
pytest --cov
```

---

## Code Quality Checks

Run Ruff:

```bash
ruff check .
```

Format code:

```bash
ruff format .
```

Run pre-commit:

```bash
pre-commit run --all-files
```

Run Bandit:

```bash
bandit -r .
```

---

## CI/CD Pipeline

GitHub Actions workflow includes:

- Ruff linting
- Code formatting checks
- Pytest execution
- PostgreSQL service container
- Docker build validation

---

## Deployment Architecture

Production deployment:

- AWS ECS → Container orchestration
- AWS RDS → PostgreSQL
- Amazon MQ → Message broker
- AWS S3 → Media/static storage
- Nginx → Reverse proxy

---

## Author

Lok Raj Kumar Vuppu

Backend: Django | DRF | Python

Frontend: React | React Native  
DevOps: Docker | AWS
