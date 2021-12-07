pipeline {
    agent { 
        dockerfile {
            filename 'Dockerfile'
            args '-u docker'
        }
    }
    stages {
        stage('Execute') {
            steps {
                sh '''
                    sudo pip install -r requirements.txt && \\
                    python3 regression.py
                '''
            }
        }
    }
}