pipeline {
    agent any
    
    stages {
        stage('Environment Setup') {
            steps {
                checkout scm
                sh 'pip install -r requirements.txt'
            }
        }
        
        stage('Pipeline Compilation') {
            steps {
                sh 'python src/pipeline_components.py' // Re-compile components just in case
                sh 'python pipeline.py'
                sh 'ls -l pipeline.yaml'
            }
        }
    }
}
