# HOTEL CANCELLATION PREDICTION – End-to-End ML Deployment Pipeline

## Project Overview

This project demonstrates a **production-grade MLOps workflow** for training, containerizing, and deploying a Machine Learning model using modern DevOps and Cloud practices.

The pipeline automates:

* Model packaging
* Docker image creation
* Image push to Google Container Registry (GCR)
* Deployment to **Google Cloud Run**
* CI/CD orchestration using **Jenkins**


##  Architecture Overview

**Tools & Technologies Used**

* **Python 3.10**
* **Flask** – Model inference API
* **LightGBM** – ML model
* **Docker** – Containerization
* **Jenkins** – CI/CD orchestration
* **Google Cloud Run** – Serverless deployment
* **Google Container Registry (GCR)** – Docker image storage
* **GitHub** – Source control


## CI/CD Workflow

1. **Code Checkout**

   * Jenkins pulls code from GitHub (`main` branch)

2. **Docker Image Build**

   * Flask application + ML model packaged into Docker image

3. **Push Image to GCR**

   * Image tagged and pushed to Google Container Registry

4. **Deploy to Cloud Run**

   * Container deployed as a serverless service
   * Public endpoint exposed automatically


## 📂 Project Structure

```text
.
├── application.py              # Flask application (model inference)
├── Dockerfile                  # Docker image definition
├── Jenkinsfile                 # Jenkins CI/CD pipeline
├── setup.py                    # Python packaging
├── requirements.txt            # Dependencies
├── config/
│   └── paths_config.py         # Centralized path management
├── artifacts/
│   ├── models/
│   │   └── lgbm_model.pkl      # Trained ML model
│   ├── raw/
│   └── processed/
├── templates/
│   └── index.html              # UI for predictions
└── src/
    └── training_pipeline/      # Model training logic
```

---

## Docker Configuration

Key points:

* Uses **Python 3.10 slim image**
* Installs required system libraries (`libgomp1`)
* Installs project in editable mode
* Exposes port **8080** (required by Cloud Run)

```dockerfile
FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -e .

EXPOSE 8080

CMD ["python", "application.py"]
```

---

## Cloud Run Deployment

* Region: `us-central1`
* Port: `8080` (mandatory)
* Public access enabled (`--allow-unauthenticated`)
* Auto-scaling enabled by default



## Model Loading Strategy

To avoid startup failures in Cloud Run, the model is **loaded lazily** (on first request):

```python
loaded_model = None

def get_model():
    global loaded_model
    if loaded_model is None:
        loaded_model = joblib.load(MODEL_OUTPUT_PATH)
    return loaded_model
```

This ensures:

* Faster container startup
* No crash during cold start
* Better Cloud Run compatibility


## Accessing the Application

After successful deployment:

1. Go to **Google Cloud Console**
2. Navigate to **Cloud Run → Services**
3. Click on your service (`ml-project`)
4. Open the **Service URL**
5. Submit inputs via the UI to get predictions


##  Cleanup Guide (Optional)

To fully clean resources after testing:

### Delete Cloud Run Service

```bash
gcloud run services delete ml-project --region us-central1
```

### Delete Docker Images from GCR

```bash
gcloud container images delete gcr.io/<PROJECT_ID>/ml-project:latest
```

### (Optional) Delete Registry Entirely

```bash
gcloud services disable containerregistry.googleapis.com
```

## Key Learnings

* Importance of **PORT=8080** in Cloud Run
* Difference between local Docker and Cloud Run execution
* Jenkins permission handling for Docker
* Lazy loading ML models in serverless environments
* End-to-end CI/CD for ML systems



## Author

**Utkrisht Mallick** <br/>
Machine Learning Engineer 

