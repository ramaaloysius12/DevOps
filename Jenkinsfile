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
                        if [ ! -d "${VENV_NAME}" ]; then
                            python3 -m venv ${VENV_NAME}
                        fi

                        . ${VENV_NAME}/bin/activate
                        pip install --upgrade pip
                        if [ -f "requirements.txt" ]; then
                            pip install -r requirements.txt
                        fi
                        pip install pytest
                    '''
                }
            }
        }

        stage('3. Run Pytest') {
            steps {
                echo 'Menjalankan unit testing dengan pytest...'
                dir('hris_web') {
                    sh '''
                        . ${VENV_NAME}/bin/activate
                        
                        # Cek apakah folder tests ada, jika tidak jalankan pytest di root atau lewati exit code 5
                        if [ -d "tests" ]; then
                            pytest -v tests/
                        else
                            echo "Folder 'tests' tidak ditemukan, menjalankan pytest di root..."
                            pytest -v || EXIT_CODE=$?
                            
                            # Jika exit code adalah 5 (tidak ada test ditemukan), anggap sukses sementara
                            if [ "${EXIT_CODE}" = "5" ]; then
                                echo "Peringatan: Belum ada file test yang ditemukan (Exit code 5)."
                                exit 0
                            elif [ "${EXIT_CODE}" != "0" ]; then
                                exit ${EXIT_CODE}
                            fi
                        fi
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
