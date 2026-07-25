from flask import Blueprint, render_template, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.data.models import Payroll

payroll_bp = Blueprint('payroll', __name__, template_folder='../../templates')

@payroll_bp.route('/payroll', methods=['GET'])
def payroll_page():
    return render_template('payroll.html')

@payroll_bp.route('/api/v1/payroll/me', methods=['GET'])
@jwt_required()
def get_my_payroll():
    # Mock Response untuk MVP
    return jsonify({
        "status": "success",
        "data": {
            "month": "Juli 2026",
            "basic_salary": 8500000,
            "allowance": 1500000,
            "deduction": 250000,
            "net_salary": 9750000
        }
    }), 200