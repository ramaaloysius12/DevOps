from flask import Blueprint, render_template, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.data.models import db, WorkReport
import uuid
from datetime import datetime

report_bp = Blueprint('report', __name__, template_folder='../../templates')

@report_bp.route('/report', methods=['GET'])
def report_page():
    return render_template('report.html')

@report_bp.route('/api/v1/report/all', methods=['GET'])
def get_all_reports():
    # Ambil semua laporan dari semua karyawan
    reports = WorkReport.query.all()
    output = [{"nama": r.employee.full_name, "judul": r.title, "deskripsi": r.description} for r in reports]
    return jsonify(output)

@report_bp.route('/api/v1/report', methods=['POST'])
@jwt_required()
def submit_report():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    new_report = WorkReport(
        employee_id=uuid.UUID(current_user_id),
        title=data['title'],
        description=data['description'],
        report_date=datetime.now().date()
    )
    db.session.add(new_report)
    db.session.commit()
    
    return jsonify({"status": "success", "message": "Laporan kerja berhasil dikirim."}), 201
