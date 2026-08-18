pipeline {
    agent any

    environment {
        VENV_NAME = 'envname'
    }

    stages {
        stage('1. Checkout Code') {
            steps {
                echo 'Mengambil kode terbaru dari repository Git...'
                checkout scm
            }
        }

        stage('2. Setup Environment & Dependencies') {
            steps {
                echo 'Memeriksa dan menyiapkan virtual environment serta dependencies...'
                dir('hris_web') {
                    sh '''
                        # Buat virtual environment jika belum ada
                        if [ ! -d "${VENV_NAME}" ]; then
                            python3 -m venv ${VENV_NAME}
                        fi

                        # Aktifkan virtual environment dan instal dependencies
                        . ${VENV_NAME}/bin/activate
                        pip install --upgrade pip
                        if [ -f "requirements.txt" ]; then
                            pip install -r requirements.txt
                        fi
                    '''
                }
            }
        }

        stage('3. Run Pytest') {
            steps {
                echo 'Menjalankan unit testing dengan pytest...'
                dir('hris_web') {
                    sh '''
                        # Aktifkan virtual environment lalu jalankan pytest
                        . ${VENV_NAME}/bin/activate
                        pytest -v
                    '''
                }
            }
        }
    }

    post {
        success {
            echo 'CI Pipeline Berhasil! Semua unit test pytest di hris_web lulus.'
        }
        failure {
            echo 'CI Pipeline Gagal! Silakan cek log pengujian pytest.'
        }
    }
}
