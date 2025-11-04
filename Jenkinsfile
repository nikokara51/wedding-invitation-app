pipeline {
  agent any
  environment {
    REGISTRY = 'docker.io'
    IMAGE = "${REGISTRY}/youruser/wedding-invite"
  }
  stages {
    stage('Checkout') {
      steps { checkout scm }
    }
    stage('Build') {
      steps {
        sh 'docker build -t $IMAGE:latest .'
      }
    }
    stage('Push') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'dockerhub', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]){
          sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
          sh 'docker push $IMAGE:latest'
        }
      }
    }
    stage('Deploy to K8s'){
      steps{
        withKubeConfig(credentialsId: 'kubeconfig'){
          sh 'kubectl apply -f k8s/deployment.yaml'
          sh 'kubectl apply -f k8s/service.yaml'
          sh 'kubectl apply -f k8s/ingress.yaml'
        }
      }
    }
  }
}
