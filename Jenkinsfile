pipeline {
    agent { 
        dockerfile {
            filename 'Dockerfile'
        }
    }
    stages {
        stage('Execute') {
            steps {
                sh '''
                    pip3 install -r requirements.txt && \\
                    python3 regression.py
                '''
            }
        }
    }
}