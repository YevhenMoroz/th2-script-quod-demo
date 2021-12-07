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
                    pip install -r requirements.txt --user && \\
                    python3 regression.py
                '''
            }
        }
    }
}