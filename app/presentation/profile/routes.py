from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.data.models import db, Employee

# 1. DEFINISIKAN BLUEPRINT TERLEBIH DAHULU DI SINI
profile_bp = Blueprint('profile', __name__)

# 2. BARU GUNAKAN DI BAWAHNYA
@profile_bp.route('/api/v1/profile', methods=['GET'])
@jwt_required()
def get_profile():
    current_user_id = get_jwt_identity() 
    employee = Employee.query.get(current_user_id)
    
    if not employee:
        return jsonify({"message": "Karyawan tidak ditemukan"}), 404
        
    return jsonify({
        "full_name": employee.full_name,
        "nik": employee.nik,
        "position": employee.position,
        "department": employee.department,
        "email": employee.email
    })