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
                    export PATH=$PATH:$WORKSPACE
                    export HOME=$WORKSPACE && \\
                    echo $HOME && \\
                    pip install -r requirements.txt --user && \\
                    python3 regression.py --user
                '''
            }
        }
    }
    post {
        cleanup {
            deleteDir()
        }        
    }
}