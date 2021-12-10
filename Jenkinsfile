pipeline {
    agent { 
        dockerfile {
            filename 'Dockerfile'
            args '-v ./log_config.conf:/var/th2/config/'   
        }
    }
    stages {
        stage('Execute') {
            steps {
                sh '''
                    export PATH=$PATH:$WORKSPACE/.local/bin/ && \\
                    export HOME=$WORKSPACE && \\
                    cd $WORKSPACE && \\
                    pip install psycopg2-binary --user && \\
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