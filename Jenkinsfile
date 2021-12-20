pipeline {
    agent { 
        dockerfile {
            filename 'Dockerfile'  
        }
    }
    parameters{
        string (name: 'NAME', defaultValue: '5.1.140.153|Regression|', description: '')
        booleanParam(name: 'ALGO', defaultValue: true, description: '')
        booleanParam(name: 'OMS', defaultValue: false, description: '')
        booleanParam(name: 'FOREX', defaultValue: false, description: '')
        booleanParam(name: 'RETAIL', defaultValue: false, description: '')
        booleanParam(name: 'WEB_ADMIN', defaultValue: false, description: '')
    }
    triggers {
        cron('')
    }

    stages {
        stage('Execute') {
            steps {
                sh '''
                    export PATH=$PATH:$WORKSPACE/.local/bin/ && \\
                    export HOME=$WORKSPACE && \\
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