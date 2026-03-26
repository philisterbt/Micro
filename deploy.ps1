# Kubernetes Deployment Script
# Bu script, Kubernetes (Minikube veya Docker Desktop K8s) ortamında mikroservisleri başlatır.

Write-Host "Deploying microservices to Kubernetes..."

# Create config and secrets first
kubectl apply -f k8s/config.yaml

# Deploy RabbitMQ
kubectl apply -f k8s/rabbitmq.yaml

# Wait a bit for RabbitMQ to start initializing
Start-Sleep -Seconds 5

# Deploy other services
kubectl apply -f k8s/auth-service.yaml
kubectl apply -f k8s/note-service.yaml
kubectl apply -f k8s/notification-service.yaml
kubectl apply -f k8s/api-gateway.yaml

Write-Host "Deployment applied. Checking pods status..."
kubectl get pods
Write-Host "System deployed successfully!"
