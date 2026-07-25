from flask import Blueprint, request, jsonify, render_template
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.data.models import db, LeaveRequest
from datetime import datetime
import uuid

leave_bp = Blueprint('leave', __name__, template_folder='../../templates')

@leave_bp.route('/leave', methods=['GET'])
def leave_page():
    return render_template('leave.html')

@leave_bp.route('/api/v1/leave/request', methods=['POST'])
@jwt_required()
def submit_leave():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    start_date = datetime.strptime(data['start_date'], "%Y-%m-%d").date()
    end_date = datetime.strptime(data['end_date'], "%Y-%m-%d").date()
    
    new_leave = LeaveRequest(
        employee_id=uuid.UUID(current_user_id),
        leave_type=data['leave_type'],
        start_date=start_date,
        end_date=end_date,
        reason=data.get('reason', '')
    )
    
    db.session.add(new_leave)
    db.session.commit()
    
    return jsonify({"status": "success", "message": "Pengajuan cuti berhasil."}), 201


@leave_bp.route('/api/v1/leave/approve', methods=['POST'])
def approve_leave():
    data = request.get_json()
    leave_id = data.get('leave_id')
    new_status = data.get('status') # 'APPROVED' atau 'REJECTED'
    
    leave_request = LeaveRequest.query.get(leave_id)
    if leave_request:
        leave_request.status = new_status
        db.session.commit()
        return jsonify({"status": "success", "message": f"Pengajuan {new_status}"}), 200
    
    return jsonify({"status": "error", "message": "Data tidak ditemukan"}), 404

@leave_bp.route('/approval', methods=['GET'])
def approval_page():
    return render_template('approval.html')

# API untuk ambil data cuti yang statusnya 'PENDING'
@leave_bp.route('/api/v1/leave/pending', methods=['GET'])
def get_pending_leaves():
    pending = LeaveRequest.query.filter_by(status='PENDING').all()
    # Ubah data ke bentuk JSON
    data = [{"id": l.id, "employee_name": l.employee.full_name, "reason": l.reason} for l in pending]
    return jsonify(data)
