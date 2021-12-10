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
                    export PATH=$PATH:$WORKSPACE/.local/bin/
                    export HOME=$WORKSPACE && \\
                    cd $WORKSPACE && \\
                    mkdir /var/th2/config && \\
                    cat ./config.conf > /var/th2/config/log_config.conf && \\
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