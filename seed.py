import bcrypt
from app import create_app
from app.data.models import db, Role, Employee
import uuid

def seed_database():
    app = create_app()
    
    with app.app_context():
        print("Mempersiapkan Database...")
        db.create_all() # Pastikan tabel ada
        
        # 1. Cek apakah role sudah ada
        role_hrd = Role.query.filter_by(name='HRD').first()
        role_karyawan = Role.query.filter_by(name='Karyawan').first()
        
        if not role_hrd:
            role_hrd = Role(name='HRD')
            db.session.add(role_hrd)
        if not role_karyawan:
            role_karyawan = Role(name='Karyawan')
            db.session.add(role_karyawan)
            
        db.session.commit()
        print("✔️ Roles berhasil dibuat.")

        # 2. Buat Akun Dummy Karyawan
        karyawan_email = 'ahmad@perusahaan.com'
        if not Employee.query.filter_by(email=karyawan_email).first():
            # Hash password "password123"
            salt = bcrypt.gensalt()
            hashed_pw = bcrypt.hashpw('password123'.encode('utf-8'), salt)
            
            new_employee = Employee(
                id=uuid.uuid4(),
                nik="KRY-2026-001",
                email=karyawan_email,
                password_hash=hashed_pw.decode('utf-8'),
                full_name="Ahmad Karyawan",
                role_id=role_karyawan.id,
                is_active=True
            )
            db.session.add(new_employee)
            db.session.commit()
            print(f"✔️ Akun Karyawan berhasil dibuat: {karyawan_email} / password123")
        else:
            print("⚠️ Akun karyawan sudah ada.")

if __name__ == '__main__':
    seed_database()