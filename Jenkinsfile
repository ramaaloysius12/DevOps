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
                sh '''
                    # 1. Buat venv langsung di root workspace jika belum ada
                    if [ ! -d "envname" ]; then
                        python3 -m venv envname
                    fi

                    # 2. Aktifkan venv dan update pip
                    . envname/bin/activate
                    pip install --upgrade pip

                    # 3. Install requirements jika ada
                    if [ -f "requirements.txt" ]; then
                        pip install -r requirements.txt
                    fi

                    # 4. Pastikan pytest terinstal
                    pip install pytest
                '''
            }
        }

        stage('3. Run Pytest') {
            steps {
                echo 'Menjalankan unit testing dengan pytest...'
                sh '''
                    # Aktifkan virtual environment lalu jalankan test_app.py di root
                    . envname/bin/activate
                    pytest -v test_app.py
                '''
            }
        }
    }

    post {
        success {
            echo 'CI Pipeline Berhasil! Semua unit test pytest lulus.'
        }
        failure {
            echo 'CI Pipeline Gagal! Silakan cek log pengujian pytest.'
        }
    }
}
