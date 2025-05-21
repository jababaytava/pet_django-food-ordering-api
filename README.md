# 🍽️ Food Ordering API

Backend for food orders with JWT authorisation, Celery, Docker and REST API.

---
## ⚙️ Stack

- Django + DRF
- JWT authorisation (`djangorestframework-simplejwt`)
- PostgreSQL / SQLite (depending on the environment)
- Celery + RabbitMQ (background processing)
- Docker + docker-compose
- Swagger UI (auto-generation of documentation)
- Tests (`pytest`, `pytest-django`)

---

## 🚀 Running in Docker

```bash
docker-compose up --build

