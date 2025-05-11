# Task 1: Creating the Backend Application

## 1. Project Setup
Created project directory and initialized the application:
```bash
mkdir app-2023mt03042
cd app-2023mt03042
```

![Project directory structure](./images/directory_structure.png)
*Figure 1: Project directory structure*

## 2. Installing Dependencies
```bash
pip install fastapi uvicorn python-dotenv
```

![Requirements file](./images/requirements.txt.png)
*Figure 2: Requirements.txt contents*

## 3. Project Structure
```
app-2023mt03042/
├── main.py
├── .env
└── requirements.txt
```

## 4. Implementation Details

### Environment Variables (.env)
```plaintext
APP_VERSION=1.0
APP_TITLE=FastAPI Application 2023mt03042
```

![Environment file](./images/env_file.png)
*Figure 3: Environment variables configuration*

### Main Application (main.py)
```python
from fastapi import FastAPI
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

# Get environment variables
APP_VERSION = os.getenv("APP_VERSION")
APP_TITLE = os.getenv("APP_TITLE")

@app.get("/get_info")
async def get_info():
    return {
        "APP_VERSION": APP_VERSION,
        "APP_TITLE": APP_TITLE
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

![Main application code](./images/main_py.png)
*Figure 4: FastAPI application implementation*

## 5. Running the Application
```bash
uvicorn main:app --reload
```

![Application running](./images/application_running.png)
*Figure 5: Application running in terminal*

![Application deployed](./images/app_deploy.png)
*Figure 6: Application endpoint response*