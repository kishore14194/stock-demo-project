pipeline {
    agent { label 'build-node' }

    environment {
        DOCKER_IMAGE = "stock-backend"
        NEXUS_HOST = "13.232.142.168"
        NEXUS_PORT = "8083" // Port for Docker repo, not Nexus UI
        NEXUS_REPO = "docker-hosted"
        IMAGE_TAG = "latest"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Docker Build') {
            steps {
                script {
                    sh "docker build -t $DOCKER_IMAGE ."
                }
            }
        }

        stage('Tag & Push to Nexus') {
            steps {
                script {
                    sh """
                        docker tag $DOCKER_IMAGE $NEXUS_HOST:$NEXUS_PORT/$DOCKER_IMAGE:$IMAGE_TAG
                        docker login $NEXUS_HOST:$NEXUS_PORT -u admin -p admin123
                        docker push $NEXUS_HOST:$NEXUS_PORT/$DOCKER_IMAGE:$IMAGE_TAG
                    """
                }
            }
        }
    }
}
