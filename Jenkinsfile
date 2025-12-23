pipeline {
    agent any

    stages {

        stage('Checkout Code') {
            steps {
                checkout scmGit(
                    branches: [[name: '*/main']],
                    userRemoteConfigs: [[
                        credentialsId: 'github-token',
                        url: 'https://github.com/utkrisht14/Mlops_Project_1'
                    ]]
                )
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                docker build -t mlops-project-1:latest .
                '''
            }
        }

        stage('Run Container (Optional)') {
            steps {
                sh '''
                docker run -d -p 5000:5000 --name mlops_app mlops-project-1:latest || true
                '''
            }
        }
    }
}
