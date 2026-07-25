from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from app.data.models import Employee

def role_required(required_role_name):
    """
    Decorator untuk membatasi akses API berdasarkan nama Role (contoh: 'HRD', 'Karyawan').
    Penggunaan: @role_required('HRD')
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            # 1. Pastikan request memiliki JWT Token yang valid
            verify_jwt_in_request()
            
            # 2. Ambil ID User dari Token
            claims = get_jwt()
            user_id = claims.get("sub")
            
            # 3. Cari User & Relasi Rolenya di Database
            user = Employee.query.get(user_id)
            if not user or not user.is_active:
                return jsonify({"message": "Akun tidak ditemukan atau tidak aktif"}), 403
                
            # Asumsi kita punya relasi ke tabel Role
            # Di SQLAlchemy model, pastikan Employee punya backref ke Role
            if getattr(user, 'role', None) and user.role.name != required_role_name:
                return jsonify({"message": f"Akses Ditolak. Membutuhkan role: {required_role_name}"}), 403
                
            return fn(*args, **kwargs)
        return decorator
    return wrapper