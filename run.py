from app import create_app
from dotenv import load_dotenv

# Muat variabel environment (Database URL, Secret Keys) dari file .env
load_dotenv()

# Inisialisasi aplikasi
app = create_app()

if __name__ == '__main__':
    # Jalankan server
    # Pastikan debug=False saat mendeploy ke server Production (Nginx/Gunicorn)
    app.run(host='0.0.0.0', port=5000, debug=True)