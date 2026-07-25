from flask import Blueprint, request, jsonify, render_template, make_response
from flask_jwt_extended import create_access_token
from app.data.models import Employee
import bcrypt

auth_bp = Blueprint('auth', __name__, template_folder='../../templates')

@auth_bp.route('/', methods=['GET'])
@auth_bp.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')

@auth_bp.route('/api/v1/auth/login', methods=['POST'])
def api_login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({"message": "Email dan Password wajib diisi"}), 400
        
    employee = Employee.query.filter_by(email=email, is_active=True).first()
    
    # Verifikasi Password Hashing
    if employee and employee.password_hash == password:
        # Buat JWT Token
        access_token = create_access_token(identity=str(employee.id))
        
        return jsonify({
            "status": "success",
            "message": "Login berhasil",
            "token": access_token,
            "data": {
                "name": employee.full_name,
                "role": employee.role_id
            }
        }), 200
        
    return jsonify({"message": "Email atau Password salah"}), 401
