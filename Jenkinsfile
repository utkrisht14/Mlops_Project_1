pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t mlops-project-1:latest .'
            }
        }

        stage('Run Container') {
            steps {
                sh '''
                docker rm -f mlops_app || true
                docker run -d -p 5000:5000 --name mlops_app mlops-project-1:latest
                '''
            }
        }
    }
}
