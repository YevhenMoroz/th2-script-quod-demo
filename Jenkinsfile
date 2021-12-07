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
                    sudo pip install -r requirements.txt --user && \\
                    python3 regression.py
                '''
            }
        }
    }
}