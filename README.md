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


Docker Image Build:
docker build -t wedding-invite-app .
docker run -p 8000:8000 wedding-invite-app

If it is working then
docker login

docker tag wedding-invite-app nikos123/wedding-invite-app:latest
docker push nikos123/wedding-invite-app:latest


Pull the image anywhere:
docker pull nikos123/wedding-invite-app:latest
docker run -p 8000:8000 nikos123/wedding-invite-app:latest



For k8s, run

kubectl apply -k k8s/overlays/

if the pod is deployed, then run

minikube service wedding-invite-service --url


For ingress and minikube:

check if ingress is enabled:
minikube addons list


If not enable it:
minikube addons enable ingress

then run:
minikube tunnel

and access the http:localhost to go to the site

