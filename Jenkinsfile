pipeline {
    agent any

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
                        # 1. Buat venv jika belum ada
                        python3 -m venv envname

                        # 2. Aktifkan venv dan upgrade pip
                        . envname/bin/activate
                        pip install --upgrade pip

                        # 3. Install requirements jika file-nya ada
                        if [ -f "requirements.txt" ]; then
                            pip install -r requirements.txt
                        fi

                        # 4. Install pytest
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
                        . envname/bin/activate
                        pytest -v test_app.py
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
