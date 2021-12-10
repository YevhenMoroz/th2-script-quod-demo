pipeline {
    agent { 
        dockerfile {
            filename 'Dockerfile'
            args '-v $HOME/log_config.conf:/var/th2/config/'   
        }
    }
    stages {
        stage('Execute') {
            steps {
                sh '''
                    export PATH=$PATH:$WORKSPACE/.local/bin/ && \\
                    export HOME=$WORKSPACE && \\
                    cd $WORKSPACE && \\
                    ls /var/th2/ && \\
                    cat /var/th2/config/log_config.conf && \\
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