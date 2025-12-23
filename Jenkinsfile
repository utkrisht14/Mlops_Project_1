pipeline {
    agent any

    environment {
        GCP_PROJECT = "my-gcp-project-478522"
        IMAGE_NAME = "gcr.io/my-gcp-project-478522/ml-project"
        GCLOUD_PATH = "/var/jenkins_home/google-cloud-sdk/bin"
    }

    stages {

        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Build & Push Docker Image to GCR') {
            steps {
                withCredentials([
                    file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')
                ]) {
                    sh """
                    export PATH=\$PATH:${GCLOUD_PATH}

                    gcloud auth activate-service-account --key-file=\$GOOGLE_APPLICATION_CREDENTIALS
                    gcloud config set project ${GCP_PROJECT}
                    gcloud auth configure-docker --quiet

                    docker build -t ${IMAGE_NAME}:latest .
                    docker push ${IMAGE_NAME}:latest
                    """
                }
            }
        }

        stage('Run Container') {
            steps {
                sh """
                docker rm -f mlops_app || true
                docker run -d -p 5000:5000 --name mlops_app ${IMAGE_NAME}:latest
                """
            }
        }
    }
}
