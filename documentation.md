### Birla Institute of Technology & Science, Pilani 
### Work Integrated Learning Programmes Division 
### Second Semester 2024-2025 
### Devops for Cloud (NSCC ZG507) Course Assignment 
### Context: 
### In this assignment, you will create a backend application using FastAPI, containerize it with Docker, deploy it in a Kubernetes cluster (Ex: Minikube) with networking and load balancing, and monitor its performance with Prometheus. You will implement, test, and monitor your application by tracking metrics like the number of requests received, CPU usage, and memory usage for each replica. Use your <roll_number> as your bits mail starting id

### Name : POKALA DEEP
### BITS-ROLL NUMBER : 2024MT03042


## Task 1: Creating the Backend Application

## 1. Project Setup
Created project directory and initialized the application:
```bash
mkdir app-2024mt03042
cd app-2024mt03042
```

## 2. Installing Dependencies
```bash
pip install fastapi uvicorn python-dotenv
```

## 3. Project Structure
```
app-2024mt03042/
├── main.py
├── .env
└── requirements.txt
```

![Project structure](./images/Project_structure.png)
*Figure 1: Project structure configuration*

## 4. Implementation Details

### Environment Variables (.env)
```plaintext
APP_VERSION=1.0
APP_TITLE=FastAPI Application 2023mt03042
```

![Environment file](./images/env_file.png)
*Figure 2: Environment variables configuration*

### Main Application (main.py)
```python
from fastapi import FastAPI , Response
from dotenv import load_dotenv
from prometheus_client import Counter, Gauge, generate_latest, CONTENT_TYPE_LATEST
from prometheus_fastapi_instrumentator import Instrumentator
import uvicorn
import psutil
import os

# Load environment variables
load_dotenv()

app = FastAPI()

# Initialize metrics
REQUEST_COUNT = Counter('get_info_requests_total', 'Total requests to /get_info')
CPU_USAGE = Gauge('cpu_usage_percent', 'CPU Usage percentage')
MEMORY_USAGE = Gauge('memory_usage_bytes', 'Memory Usage percentage')


# Add Prometheus instrumentation
instrumentator = Instrumentator()
instrumentator.instrument(app).expose(app)


# Get environment variables
APP_VERSION = os.getenv("APP_VERSION")
APP_TITLE = os.getenv("APP_TITLE")

@app.get("/get_info")
async def get_info():
    REQUEST_COUNT.inc()
    return {
        "APP_VERSION": APP_VERSION,
        "APP_TITLE": APP_TITLE
    }

@app.get("/metrics")
def metrics():
    CPU_USAGE.set(psutil.cpu_percent())
    MEMORY_USAGE.set(psutil.virtual_memory().percent)

    return Response (generate_latest(), media_type=CONTENT_TYPE_LATEST)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## 5. Running the Application
```bash
uvicorn main:app --reload
```

![Application running](./images/application_running.png)
*Figure 3: Application running in terminal*

![Application deployed](./images/local_deploy.png)
*Figure 4: Application endpoint response*



## Task 2: Dockerizing the Backend Application

### 1. Docker Setup
Verified Docker installation on EC2 instance:
```bash
docker --version
```
![Docker Version](./images/docker_version_check.png)
*Figure 5: Docker version verification*

### 2. Dockerfile Creation
```dockerfile
FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY main.py .
COPY .env .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 3. Docker Image Build
```bash
docker build -t img-2024mt03042 .
```
![Docker Build](./images/docker_build_op.png)
*Figure 6: Docker image build process*

### 4. Image Verification
```bash
docker images | grep img-2024mt03042
```
![Docker Images](./images/docker_images_op.png)
*Figure 7: Docker image verification*

## Task 3: Running Docker Container

### 1. Container Creation
```bash
docker run -d -p 8000:8000 --name cnr-2024mt03042 img-2024mt03042
```
![Container Running](./images/docker_run.png)
*Figure 8: Docker container running status*

### 2. Container Verification
```bash
docker ps | grep cnr-2024mt03042
```
![Container Status](./images/docker_cnr_image.png)
*Figure 9: Docker container verification*

### 3. Application Access
Accessed the application through browser:
- URL: http://44.223.48.221:8000/get_info
![Browser Access](./images/docker_deploy.png)
*Figure 10: Application access through browser*

### 4. API Response
```json
{
    "APP_VERSION": "1.0",
    "APP_TITLE": "FastAPI Application 2024mt03042"
}
```
![API Response](./images/docker_deploy.png)
*Figure 11: API endpoint response*

## Project Structure
```
app-2024mt03042/
├── venv/
├── main.py
├── requirements.txt
├── .env
├── Dockerfile
└── documentation.md
```


## Task 4: Kubernetes Deployment

### 1. ConfigMap Creation
Created ConfigMap to store environment variables:
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: config-2024mt03042
data:
  APP_VERSION: "1.0"
  APP_TITLE: "FastAPI Application 2024mt03042"
```

### 2. Deployment Configuration
Created deployment with 2 replicas:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fastapi-deployment-2024mt03042
spec:
  replicas: 2
  selector:
    matchLabels:
      app: fastapi-2024mt03042
  template:
    metadata:
      labels:
        app: fastapi-2024mt03042
    spec:
      containers:
      - name: fastapi-container
        image: img-2024mt03042:latest
        imagePullPolicy: IfNotPresent
        ports:
        - containerPort: 8000
        envFrom:
        - configMapRef:
            name: config-2024mt03042
```

### 3. Service Configuration
Created NodePort service for external access:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: fastapi-service-2024mt03042
spec:
  type: NodePort
  selector:
    app: fastapi-2024mt03042
  ports:
  - port: 8000
    targetPort: 8000
    nodePort: 30000
```

### 4. Deployment Verification

#### ConfigMap Status
```bash
$ kubectl describe configmap config-2024mt03042
Name:         config-2024mt03042
Namespace:    default
Data:
  APP_TITLE:  FastAPI Application 2024mt03042
  APP_VERSION: 1.0
```
![ConfigMap Status](./images/configmap.png)
*Figure 12: ConfigMap Configuration*

#### Pod Status
```bash
$ kubectl get pods
NAME                                              READY   STATUS    RESTARTS   AGE
fastapi-deployment-2024mt03042-6ff7bfc77f-2pbt2   1/1     Running   0          5m30s
fastapi-deployment-2024mt03042-6ff7bfc77f-j58jk   1/1     Running   0          5m30s
```
![Pod Status](./images/pods_get.png)
*Figure 13: Running Pods*

#### Service Status
```bash
$ kubectl get services fastapi-service-2024mt03042
NAME                          TYPE       CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE
fastapi-service-2024mt03042   NodePort   10.108.148.140   <none>      8000:30000/TCP   13m
```
![Service Status](./images/service.png)
*Figure 14: Service Configuration*

### 5. Application Testing
Testing the deployed application:
```bash
$ curl -v $(minikube service fastapi-service-2024mt03042 --url)/get_info
{
    "APP_VERSION": "1.0",
    "APP_TITLE": "FastAPI Application 2024mt03042"
}
```
![API Response](./images/api_response.png)
*Figure 15: API Response from Kubernetes*

### 6. Verification Commands
```bash
# Check deployment status
kubectl get deployments
NAME                             READY   UP-TO-DATE   AVAILABLE   AGE
fastapi-deployment-2024mt03042   2/2     2            2           5m53s

# Check pod logs
kubectl logs fastapi-deployment-2024mt03042-6ff7bfc77f-2pbt2
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

## Task 5: Load Balancer Configuration

### 1. Service Configuration Update
Changed service type from NodePort to LoadBalancer:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: fastapi-service-2024mt03042
spec:
  type: LoadBalancer
  selector:
    app: fastapi-2024mt03042
  ports:
  - port: 8000
    targetPort: 8000
```

### 2. Load Balancer Deployment
```bash
# Apply LoadBalancer service
kubectl apply -f k8s/service-2024mt03042.yaml

```bash
(venv) ubuntu@ip-172-31-29-152:~/app-2024mt03042/k8s$ kubectl apply -f service-2024mt03042.yaml
service/fastapi-service-2024mt03042 configured
```

# Enable external access
minikube tunnel
```bash
![LoadBalancer Service](./images/tunnel.png)
*Figure 16: LoadBalancer Service Configuration*
```

### 3. Pod Logs Analysis
```bash
# View logs from both pods
kubectl logs -l app=fastapi-2024mt03042
```
![Pod Logs](./images/pod_logs.png)
*Figure 17: Request Distribution in Pod Logs*

```bash
### 4. Load Balancer Setup & Service Status
```bash
# Terminal 1: Start tunnel (keep running)
minikube tunnel

# Terminal 2: Verify service
```bash
kubectl get services fastapi-service-2024mt03042
```
![Service Status](./images/service_status_load_balancer.png)
*Figure 18: LoadBalancer Service Status*

## 5. Load Balancing Proof
```bash
# Get pod names
POD1=$(kubectl get pods -l app=fastapi-2024mt03042 -o jsonpath='{.items[0].metadata.name}')
POD2=$(kubectl get pods -l app=fastapi-2024mt03042 -o jsonpath='{.items[1].metadata.name}')

# Make multiple requests
for i in {1..10}; do
    curl http://localhost:8000/get_info
    echo "Request $i completed"
done

# View distribution in pod logs
echo "=== Pod 1 ($POD1) Logs ==="
kubectl logs $POD1
echo "=== Pod 2 ($POD2) Logs ==="
kubectl logs $POD2
```
![Load Balance Distribution](./images/load_balancer_distribuition.png)
*Figure 18: Request Distribution Across Pods*



## Task 5: Prometheus  Monitoring
## 1. Prometheus yaml file to add:

```bash
apiVersion: v1
kind: ConfigMap
metadata:
  name: prometheus-config
data:
  prometheus.yml: |
    global:
      scrape_interval: 15s
    scrape_configs:
      - job_name: 'fastapi'
        static_configs:
          - targets: ['fastapi-service-2024mt03042:8000']
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: prometheus
  namespace: monitoring
spec:
  replicas: 1
  selector:
    matchLabels:
      app: prometheus
  template:
    metadata:
      labels:
        app: prometheus
    spec:
      containers:
        - name: prometheus
          image: prom/prometheus:v2.45.0
          ports:
            - containerPort: 9090
          volumeMounts:
            - name: config-volume
              mountPath: /etc/prometheus/
          args:
            - '--config.file=/etc/prometheus/prometheus.yml'
            - '--storage.tsdb.path=/prometheus'
            - '--web.console.libraries=/etc/prometheus/console_libraries'
            - '--web.console.templates=/etc/prometheus/consoles'
      volumes:
        - name: config-volume
          configMap:
            name: prometheus-config
---
apiVersion: v1
kind: Service
metadata:
  name: prometheus-service
  namespace: monitoring
spec:
  type: LoadBalancer
  selector:
    app: prometheus
  ports:
    - port: 9090
      targetPort: 9090
      nodePort: 30000
```

## 2. Status of the running pods and prometheus
```bash
Deploy the prometheus app  kubectl apply -f k8s/prometheus-deployment
Get pods to see if the promethus container is running
$ kubectl get pods
NAME                                              READY   STATUS    RESTARTS   AGE
fastapi-deployment-2024mt03042-6ff7bfc77f-2pbt2   1/1     Running   0          16m
fastapi-deployment-2024mt03042-6ff7bfc77f-j58jk   1/1     Running   0          16m
prometheus-7dcb8c8489-5kw2t                       1/1     Running   0          22m
```
## 3. running with minikube ip to check the serivce url
```bash
Now, run
5$ minikube service prometheus-service
|-----------|--------------------|-------------|---------------------------|
| NAMESPACE |        NAME        | TARGET PORT |            URL            |
|-----------|--------------------|-------------|---------------------------|
| default   | prometheus-service |        9090 | http://192.168.49.2:30000 |
|-----------|--------------------|-------------|---------------------------|
🎉  Opening service default/prometheus-service in default browser...

```
![Load Balance Distribution](./images/prom_cpu.png)
*Figure 19: CPU monitoring Across Pods*

![Load Balance Distribution](./images/prom_memory.png)
*Figure 20: Memory monitoring Across Pods*

![Load Balance Distribution](./images/prome_requests.png)
*Figure 21: Request monitoring Across Pods*


## Challenges Encountered

1. **Docker Port Mapping**
   - Challenge: Application wasn't accessible from browser
   - Solution: Correctly mapped ports with -p 8000:8000

2. **Security Group Configuration** {optional as i used ec2 instance for the installation of docker and k8}
   - Challenge: Couldn't access application from outside EC2
   - Solution: Added inbound rule for port 8000 in security group

3. **Image Accessibility**
   - Challenge: Minikube couldn't access local Docker image
   - Solution: Used `minikube image load` to make image available

4. **Prometheus Montioring**
   - Challenge:  Initially was not able to access the prometheus server on the browser
   - Solution: Security Groups in Ec2 werent allowing me to do , had to open the port 3000 accordingly to make to work
