# Wedding Invite App

A personalized wedding invitation web app built with FastAPI, Jinja2 templates, Docker, Kubernetes and Jenkins.

## Quickstart (local)

1. Copy `.env.example` to `.env` and fill values.
2. Install dependencies: `pip install -r requirements.txt`
3. Initialize DB: `python -c "import app.database"`
4. Run: `uvicorn app.main:app --reload --port 8000`
5. Visit `http://localhost:8000/invite/demo`

## Deploy
Build the Docker image, push to a registry, then apply the k8s manifests. Store secrets in Kubernetes secrets.
