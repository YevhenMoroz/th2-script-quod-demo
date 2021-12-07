pipeline {
    agent { 
        dockerfile {
            filename 'Dockerfile'
            arg '-v /var/th2/config/log_config.conf:./config.conf'
        }
    }
    stages {
        stage('Execute') {
            steps {
                sh '''
                    export PATH=$PATH:$WORKSPACE/.local/bin/
                    export HOME=$WORKSPACE && \\
                    echo $HOME && \\
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