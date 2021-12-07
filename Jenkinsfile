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
                    python3 -m pip install -r requirements.txt --user && \\
                    python3 regression.py
                '''
            }
        }
    }
}