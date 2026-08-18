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
                    # Hapus folder venv lama jika ada untuk menghindari file corrupt/hilang
                    rm -rf envname

                    # Buat virtual environment baru yang bersih
                    python3 -m venv envname

                    # Aktifkan virtual environment dan update pip
                    . envname/bin/activate
                    pip install --upgrade pip

                    # Install requirements.txt jika ada
                    if [ -f "requirements.txt" ]; then
                        pip install -r requirements.txt
                    fi

                    # Pastikan pytest terinstal
                    pip install pytest
                '''
            }
        }

        stage('3. Run Pytest') {
            steps {
                echo 'Menjalankan unit testing dengan pytest...'
                sh '''
                    # Aktifkan virtual environment lalu jalankan test_app.py
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
