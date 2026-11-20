# Flask + MongoDB Deployment on Kubernetes (Minikube)

A containerized Python Flask REST API connected to an authenticated MongoDB database, orchestrated on a local Minikube Kubernetes cluster with persistent storage, internal DNS service discovery, resource management, and CPU-based Horizontal Pod Autoscaling (HPA).

---

## Project Structure

```text
faralpha-kubernetes-assignment/
│
├── app/
│   ├── app.py                 # Flask application with MongoDB auth & health endpoint
│   ├── requirements.txt       # Python dependencies
│   └── Dockerfile             # Container image definition for Flask app
│
├── kubernetes/
│   ├── mongo-secret.yaml      # Kubernetes Secret for MongoDB root credentials
│   ├── mongo-pv-pvc.yaml      # PersistentVolume and PersistentVolumeClaim for /data/db
│   ├── mongo-statefulset.yaml # MongoDB StatefulSet with authentication enabled
│   ├── mongo-service.yaml     # Internal ClusterIP Service for MongoDB
│   ├── flask-deployment.yaml  # Flask Deployment (2 replicas, probes, resource limits)
│   ├── flask-service.yaml     # NodePort Service exposing Flask externally
│   └── flask-hpa.yaml         # HorizontalPodAutoscaler (2 to 5 replicas at 70% CPU)
│
├── screenshots/               # Verification screenshots of cluster, endpoints & HPA
└── README.md                  # Deployment guide, architecture explanations & test results