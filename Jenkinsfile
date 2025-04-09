pipeline {
    agent { label 'build-node' }

    environment {
        DOCKER_IMAGE = "stock-backend"
        NEXUS_URL = "13.233.129.221:8083"
        NEXUS_REPO = "docker-hosted"
        IMAGE_TAG = "latest"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        // stage('Test Docker Access') {
        //     steps {
        //         sh 'bash -c "whoami && docker ps"'
        //     }
        // }

        // stage('Docker Build') {
        //     steps {
        //         script {
        //             sh "docker build -t $DOCKER_IMAGE ."
        //         }
        //     }
        // }

         stage('Debug Docker') {
            steps {
                sh '''
                    sudo su - ubuntu
                    echo "Current PATH: $PATH"
                    echo "Whoami: $(whoami)"
                    echo "Docker path: $(which docker)"
                    /usr/bin/docker --version
                '''
            }
        }

        

        stage('Tag & Push to Nexus') {
            steps {
                script {
                    sh """
                        docker tag $DOCKER_IMAGE $NEXUS_URL/$NEXUS_REPO/$DOCKER_IMAGE:$IMAGE_TAG
                        docker login $NEXUS_URL -u admin -p your-nexus-password
                        docker push $NEXUS_URL/$NEXUS_REPO/$DOCKER_IMAGE:$IMAGE_TAG
                    """
                }
            }
        }
    }
}
