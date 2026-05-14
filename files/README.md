# Flask Docker App — CI/CD Pipeline

A production-ready **Flask REST API** containerized with **Docker** and automated with a **GitHub Actions CI/CD pipeline**.

---

## 📁 Project Structure

```
flask-docker-app/
├── app/
│   ├── __init__.py        # App factory
│   └── routes.py          # REST endpoints
├── tests/
│   └── test_routes.py     # Pytest test suite
├── .github/
│   └── workflows/
│       └── ci-cd.yml      # GitHub Actions pipeline
├── run.py                 # Entry point (Gunicorn target)
├── Dockerfile             # Multi-stage production build
├── docker-compose.yml     # Local dev / test orchestration
├── requirements.txt
├── .dockerignore
└── .gitignore
```

---

## 🚀 REST API Endpoints

| Method | Endpoint         | Description          |
|--------|-----------------|----------------------|
| GET    | `/`             | Health check         |
| GET    | `/items`        | List all items       |
| GET    | `/items/<id>`   | Get item by ID       |
| POST   | `/items`        | Create a new item    |
| PUT    | `/items/<id>`   | Update an item       |
| DELETE | `/items/<id>`   | Delete an item       |

### Example — Create an item
```bash
curl -X POST http://localhost:5000/items \
     -H "Content-Type: application/json" \
     -d '{"name": "Widget", "description": "A cool widget"}'
```

---

## 🐳 Running with Docker

### Build & run (single container)
```bash
docker build -t flask-docker-app .
docker run -d -p 5000:5000 --name flask_api flask-docker-app
```

### With Docker Compose
```bash
# Start the API
docker compose up -d

# Run tests in a container
docker compose --profile test up test

# Stop everything
docker compose down
```

---

## 🧪 Running Tests Locally

```bash
pip install -r requirements.txt
pytest tests/ -v --cov=app --cov-report=term-missing
```

---

## ⚙️ CI/CD Pipeline (GitHub Actions)

The pipeline (`.github/workflows/ci-cd.yml`) runs on every push/PR and has **3 jobs**:

```
Push to main
    │
    ▼
┌─────────────┐
│  1. Test    │  Install deps → Run pytest → Upload coverage
└──────┬──────┘
       │ (pass)
       ▼
┌─────────────┐
│  2. Build   │  docker buildx → Push to Docker Hub (sha + latest tags)
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  3. Deploy  │  SSH into server → docker pull → restart container
└─────────────┘
```

### Required GitHub Secrets

| Secret               | Description                          |
|----------------------|--------------------------------------|
| `DOCKERHUB_USERNAME` | Your Docker Hub username             |
| `DOCKERHUB_TOKEN`    | Docker Hub access token              |
| `SERVER_HOST`        | Production server IP / hostname      |
| `SERVER_USER`        | SSH username on production server    |
| `SERVER_SSH_KEY`     | Private SSH key for the server       |

Add them under **Settings → Secrets and variables → Actions** in your GitHub repo.

---

## 🔒 Security Highlights

- **Non-root user** inside the container (`appuser`)
- **Multi-stage build** — build tools are never shipped to production
- **`.dockerignore`** keeps secrets and dev files out of the image
- **Gunicorn** as the production WSGI server (not Flask's dev server)

---

## 👤 Author

**Karthik Chitra** — [github.com/karthikchitra](https://github.com/karthikchitra)
