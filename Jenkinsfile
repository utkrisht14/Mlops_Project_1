pipeline {
    agent any

    environment {
        GCP_PROJECT = "my-gcp-project-478522"
        IMAGE_NAME = "gcr.io/my-gcp-project-478522/ml-project"
        GCLOUD_PATH = "/var/jenkins_home/google-cloud-sdk/bin"
        REGION = "us-central1"
        SERVICE_NAME = "ml-project"
    }

    stages {

        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Authenticate to GCP & Configure Docker') {
            steps {
                withCredentials([
                    file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')
                ]) {
                    sh """
                    export PATH=\$PATH:${GCLOUD_PATH}

                    gcloud auth activate-service-account \
                        --key-file=\$GOOGLE_APPLICATION_CREDENTIALS

                    gcloud config set project ${GCP_PROJECT}

                    gcloud auth configure-docker --quiet
                    """
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh """
                docker build -t ${IMAGE_NAME}:latest .
                """
            }
        }

        stage('Push Image to Google Container Registry') {
            steps {
                sh """
                docker push ${IMAGE_NAME}:latest
                """
            }
        }

        stage('Deploy to Google Cloud Run') {
            steps {
                sh """
                export PATH=\$PATH:${GCLOUD_PATH}

                gcloud run deploy ${SERVICE_NAME} \
                    --image ${IMAGE_NAME}:latest \
                    --platform managed \
                    --region ${REGION} \
                    --allow-unauthenticated \
                    --quiet
                """
            }
        }
    }

    post {
        success {
            echo "Pipeline completed successfully!"
        }
        failure {
            echo "Pipeline failed. Check logs above."
        }
    }
}
