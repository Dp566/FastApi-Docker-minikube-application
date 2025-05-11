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
