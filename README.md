# fastapi-deploy-lab

A minimal FastAPI application built as a hands-on lab to understand a complete, real-world deployment pipeline. 
From local code to a live, HTTPS-secured domain.

## Purpose

This project is intentionally simple on the application side (a "Hello World" API). The goal isn't the code itself — it's mastering every step of the deployment pipeline that sits behind it, before applying the same flow to more complex, production projects (like [digital_menu](https://github.com/luccatrevisan/digital_menu)).

Rather than waiting to containerize and deploy a larger system, this lab isolates the deployment pipeline as its own subject of study.

## Pipeline

```
FastAPI
   ↓
Docker
   ↓
GitHub
   ↓
GitHub Actions (CI)
   ↓
Docker Hub
   ↓
AWS EC2 (Ubuntu)
   ↓
Nginx (reverse proxy)
   ↓
HTTPS (Let's Encrypt)
   ↓
luccatrevisan.dev
```

## Live Demo

🔗 [https://luccatrevisan.dev](https://luccatrevisan.dev)
🔗 [https://luccatrevisan.dev/health](https://luccatrevisan.dev/health)

## Tech Stack

- **API:** Python 3.13, FastAPI, Uvicorn
- **Containerization:** Docker
- **CI/CD:** GitHub Actions
- **Registry:** Docker Hub
- **Infrastructure:** AWS EC2 (Ubuntu)
- **Reverse Proxy:** Nginx
- **TLS/SSL:** Let's Encrypt (Certbot)
- **DNS:** Hostinger

## Endpoints

| Method | Path      | Description                   |
|--------|-----------|-------------------------------|
| GET    | `/`       | Returns a simple greeting     |
| GET    | `/health` | Health check endpoint         |
| GET    | `/docs`   | Documentation from Swagger    |

## Running Locally

```bash
# Clone the repository
git clone https://github.com/luccatrevisan/fastapi-deploy-lab.git
cd fastapi-deploy-lab

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows

# Install dependencies
pip install -r requirements.txt

# Run the app
uvicorn src.main:app --reload
```

The API will be available at `http://localhost:8000`.

## Running with Docker

```bash
docker build -t fastapi-deploy-lab .
docker run -p 8000:8000 fastapi-deploy-lab
```

## CI/CD

Every push to `main` triggers a GitHub Actions workflow that builds the Docker image and pushes it to Docker Hub, tagged both as `latest` and with the commit SHA for traceability.

The deployed instance on EC2 pulls the updated image manually for now. A future iteration of this lab may automate that step as well (e.g. via a self-hosted runner or a webhook-triggered pull).

## Technical Decisions

- **`0.0.0.0` as the bind host:** Uvicorn must bind to `0.0.0.0` - not `127.0.0.1` - inside a container, otherwise the process only accepts connections from within the container itself, and external traffic never reaches it, even with the port correctly published.
- **Nginx as a reverse proxy instead of exposing Uvicorn directly:** the application container only accepts connections on an internal port (8000), never directly on 80/443. Nginx sits in front, handling public traffic and, eventually, TLS termination — a closer approximation of how production systems are typically structured.
- **Two image tags per build (`latest` + commit SHA):** always having a "current" tag for convenience, while retaining a permanent, traceable reference to exactly which commit produced which image.

## Motivation

This lab exists to close a specific gap: hands-on, real deployment experience with the same rigor applied to [digital_menu](https://github.com/luccatrevisan/digital_menu)'s backend architecture. Understanding *why* each layer of this pipeline exists (not just how to copy-paste the commands) is the actual goal here. The project also can improve with docker compose, testing, automatic EC2 pull, dealing with databases and other improvements.

## License

MIT