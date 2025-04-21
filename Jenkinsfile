pipeline {
    agent { label 'worker-node' }

    environment {
        DOCKER_IMAGE = "stock-backend"
        IMAGE_TAG = "latest"
        NEXUS_HOST = "${env.NEXUS_SONAR_HOST}"
        NEXUS_PORT = "8083"
        NEXUS_REPO = "docker-hosted"
        SONAR_HOST_URL = "http://${env.NEXUS_SONAR_HOST}:9000"
        SONAR_PROJECT_KEY = "stock-backend"
        SONAR_LOGIN = credentials('sonar-token') // Store your token in Jenkins credentials
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-creds')
        DOCKERHUB_REPO = "kish063/stock-backend"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('SonarQube Scan') {
            steps {
                withSonarQubeEnv('SonarQube') {
                    sh """
                        sonar-scanner \
                        -Dsonar.projectKey=$SONAR_PROJECT_KEY \
                        -Dsonar.sources=. \
                        -Dsonar.host.url=$SONAR_HOST_URL \
                        -Dsonar.login=$SONAR_LOGIN
                    """
                }
            }
        }

        stage('Docker Build') {
            steps {
                script {
                    sh "docker build -t $DOCKER_IMAGE:$IMAGE_TAG ."
                }
            }
        }

        stage('Tag & Push to Nexus') {
            steps {
                script {
                    sh """
                        docker tag $DOCKER_IMAGE:$IMAGE_TAG $NEXUS_HOST:$NEXUS_PORT/$DOCKER_IMAGE:$IMAGE_TAG
                        docker login $NEXUS_HOST:$NEXUS_PORT -u admin -p admin123
                        docker push $NEXUS_HOST:$NEXUS_PORT/$DOCKER_IMAGE:$IMAGE_TAG
                    """
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    sh """
                        echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin
                        docker tag $DOCKER_IMAGE:$IMAGE_TAG $DOCKERHUB_REPO:$IMAGE_TAG
                        docker push $DOCKERHUB_REPO:$IMAGE_TAG
                    """
                }
            }
        }
    }
}
