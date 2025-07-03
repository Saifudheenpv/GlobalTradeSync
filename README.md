GlobalTradeSync
A cloud-native platform simulating a global trade logistics system for multinational corporations (MNCs). This project demonstrates a microservices architecture deployed using Docker and Kubernetes, with plans for Helm chart integration.
Overview
GlobalTradeSync is a logistics management system designed to track cargo, manage inventory, and provide delivery analytics. It consists of three microservices and a PostgreSQL database, deployed locally with Docker and on a Kubernetes cluster using Minikube.
Features

Cargo Service: Tracks cargo details (e.g., location, status) via /cargo/{cargo_id}.
Inventory Service: Manages inventory stock levels via /inventory/{cargo_id}.
Analytics Service: Calculates delivery time since last inventory update via /analytics/{cargo_id}.
PostgreSQL Database: Stores inventory data, accessible by inventory and analytics services.

Project Phases
Phase 1: Initial Setup and Planning

Objective: Designed a microservices-based logistics system with cargo tracking, inventory management, and analytics.
Activities:
Defined architecture: Three FastAPI microservices (cargo, inventory, analytics) with a PostgreSQL database.
Set up project structure: GlobalTradeSync/cargo_service, inventory_service, analytics_service, and db.
Created GitHub repository: github.com/Saifudheenpv/GlobalTradeSync.



Phase 2: Local Development with Docker

Objective: Built and tested microservices locally using Docker.
Activities:
Developed FastAPI services:
Cargo Service: Mock data endpoint at /cargo/{cargo_id}.
Inventory Service: Queries PostgreSQL for inventory data.
Analytics Service: Calculates delivery time based on inventory data.


Created Dockerfiles for each service:
Base image: python:3.9-slim.
Installed dependencies: fastapi, uvicorn, psycopg2-binary.


Set up PostgreSQL container:docker run -d --name globaltradesync-db --network globaltradesync-network -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=shanu9090 -e POSTGRES_DB=globaltradesync postgres:13


Tested endpoints:
curl http://localhost:8000/cargo/cargo_001
curl http://localhost:8001/inventory/cargo_001
curl http://localhost:8002/analytics/cargo_001





Phase 3: Docker Compose

Objective: Orchestrated microservices and database using Docker Compose.
Activities:
Created docker-compose.yml to define services and network:version: '3.8'
services:
  cargo-api:
    build: ./cargo_service
    ports:
      - "8000:8000"
    networks:
      - globaltradesync-network
  inventory-api:
    build: ./inventory_service
    ports:
      - "8001:8000"
    networks:
      - globaltradesync-network
  analytics-api:
    build: ./analytics_service
    ports:
      - "8002:8000"
    networks:
      - globaltradesync-network
  db:
    image: postgres:13
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: shanu9090
      POSTGRES_DB: globaltradesync
    networks:
      - globaltradesync-network
networks:
  globaltradesync-network:
    driver: bridge


Ran services:docker-compose up -d


Initialized database with inventory table:CREATE TABLE inventory (
    cargo_id VARCHAR(50) PRIMARY KEY,
    stock INTEGER NOT NULL,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
INSERT INTO inventory (cargo_id, stock) VALUES
    ('cargo_001', 100),
    ('cargo_002', 50);





Phase 4: Docker Image Push

Objective: Built and pushed Docker images to Docker Hub for Kubernetes deployment.
Activities:
Built and tagged images:cd cargo_service
docker build -t saifudheenpv/globaltradesync-api:latest .
docker push saifudheenpv/globaltradesync-api:latest
cd ../inventory_service
docker build -t saifudheenpv/globaltradesync-inventory:latest .
docker push saifudheenpv/globaltradesync-inventory:latest
cd ../analytics_service
docker build -t saifudheenpv/globaltradesync-analytics:latest .
docker push saifudheenpv/globaltradesync-analytics:latest


Verified images on Docker Hub.



Phase 5: Kubernetes Setup with Minikube

Objective: Set up a local Kubernetes cluster using Minikube.
Activities:
Installed Minikube: minikube.sigs.k8s.io.
Installed kubectl: kubernetes.io/docs/tasks/tools.
Started Minikube:minikube start --driver=docker





Phase 6: Kubernetes Deployment

Objective: Deployed microservices and PostgreSQL to Minikube.
Activities:
Created Kubernetes manifests:
db/k8s/postgres-deployment.yaml for PostgreSQL.
cargo_service/k8s/deployment.yaml for cargo service.
inventory_service/k8s/deployment.yaml for inventory service.
analytics_service/k8s/deployment.yaml for analytics service.


Deployed:kubectl apply -f db/k8s/postgres-deployment.yaml
kubectl apply -f cargo_service/k8s/deployment.yaml
kubectl apply -f inventory_service/k8s/deployment.yaml
kubectl apply -f analytics_service/k8s/deployment.yaml


Ran Minikube tunnel for NodePort access:minikube tunnel


Accessed services:minikube service cargo-api-service --url
minikube service inventory-api-service --url
minikube service analytics-api-service --url


Tested endpoints:
curl http://127.0.0.1:40027/cargo/cargo_001
curl http://127.0.0.1:38393/inventory/cargo_001
curl http://127.0.0.1:43551/analytics/cargo_001
curl http://127.0.0.1:43551/analytics/cargo_999





Phase 7: Fix Database Connectivity

Objective: Resolved database connectivity issues for inventory and analytics services.
Activities:
Fixed postgres-deployment.yaml to ensure globaltradesync-db-service is correctly deployed in the default namespace with proper labels.
Updated inventory_service/main.py and analytics_service/main.py to use host="globaltradesync-db-service".
Rebuilt and pushed Docker images:cd inventory_service
docker build -t saifudheenpv/globaltradesync-inventory:latest .
docker push saifudheenpv/globaltradesync-inventory:latest
cd ../analytics_service
docker build -t saifudheenpv/globaltradesync-analytics:latest .
docker push saifudheenpv/globaltradesync-analytics:latest


Redeployed services:kubectl apply -f inventory_service/k8s/deployment.yaml
kubectl apply -f analytics_service/k8s/deployment.yaml
kubectl delete pod -l app=inventory-api
kubectl delete pod -l app=analytics-api


Verified database connectivity:kubectl exec -it $(kubectl get pod -l app=globaltradesync-db -o jsonpath="{.items[0].metadata.name}") -- psql -U postgres -d globaltradesync


Tested all endpoints successfully.



Phase 8: Helm Chart (In Progress)

Objective: Package Kubernetes deployments into a Helm chart for streamlined management.
Activities:
Install Helm.
Create and configure Helm chart.
Deploy and test services via Helm.



Prerequisites

Docker: Install Docker
Docker Compose: Install Docker Compose
Minikube: Install Minikube
kubectl: Install kubectl
Helm (Phase 8): Install Helm
Git: To clone the repository.
Python 3.9: For local development.
Docker Hub Account: For pushing images (username: saifudheenpv).

Setup Instructions
Clone Repository
git clone https://github.com/Saifudheenpv/GlobalTradeSync.git
cd GlobalTradeSync

Local Deployment (Docker)

Build and run services:docker-compose up -d


Initialize database:docker exec -it globaltradesync-db psql -U postgres -d globaltradesync

CREATE TABLE inventory (
    cargo_id VARCHAR(50) PRIMARY KEY,
    stock INTEGER NOT NULL,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
INSERT INTO inventory (cargo_id, stock) VALUES
    ('cargo_001', 100),
    ('cargo_002', 50);


Test endpoints:curl http://localhost:8000/cargo/cargo_001
curl http://localhost:8001/inventory/cargo_001
curl http://localhost:8002/analytics/cargo_001



Kubernetes Deployment (Minikube)

Start Minikube:minikube start --driver=docker


Deploy services:kubectl apply -f db/k8s/postgres-deployment.yaml
kubectl apply -f cargo_service/k8s/deployment.yaml
kubectl apply -f inventory_service/k8s/deployment.yaml
kubectl apply -f analytics_service/k8s/deployment.yaml


Run Minikube tunnel (in a separate terminal):minikube tunnel


Access services:minikube service cargo-api-service --url
minikube service inventory-api-service --url
minikube service analytics-api-service --url


Test endpoints (replace URLs with output from above):curl http://127.0.0.1:40027/cargo/cargo_001
curl http://127.0.0.1:38393/inventory/cargo_001
curl http://127.0.0.1:43551/analytics/cargo_001
curl http://127.0.0.1:43551/analytics/cargo_999



Troubleshooting

Docker: Ensure all services are running (docker ps) and the network is set up (docker network ls).
Kubernetes: Check pod status (kubectl get pods), logs (kubectl logs <pod-name>), and describe resources (kubectl describe pod <pod-name>).
Database Connectivity: Verify service (kubectl get services -l app=globaltradesync-db) and DNS (kubectl exec -it <pod-name> -- nslookup globaltradesync-db-service).
Minikube Tunnel: Keep the tunnel running for NodePort access.

Next Steps

Complete Phase 8: Deploy services using a Helm chart.
Explore CI/CD integration with GitHub Actions.
Scale the application for production with cloud providers (e.g., AWS, GCP).

Contact

GitHub: Saifudheenpv
Email: [Your Email]
LinkedIn: [Your LinkedIn]
