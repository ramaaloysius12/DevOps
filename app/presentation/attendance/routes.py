from flask import Blueprint, request, jsonify, render_template
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.core.location import GeofencingVerifier
from app.data.models import db, Attendance
from datetime import datetime
import uuid

attendance_bp = Blueprint('attendance', __name__, template_folder='../../templates')

# Koordinat Kantor Pusat (Sebagai Contoh)
OFFICE_LAT = -6.2088
OFFICE_LONG = 106.8456

@attendance_bp.route('/attendance/checkin', methods=['GET'])
def checkin_page():
    return render_template('attendance.html')

@attendance_bp.route('/api/v1/attendance/check-in', methods=['POST'])
@jwt_required()
def process_check_in():
    current_user_id = get_jwt_identity()
    data = request.get_json()

    if not data or 'latitude' not in data or 'longitude' not in data or 'photo' not in data:
        return jsonify({"status": "error", "message": "Payload tidak lengkap"}), 400

    user_lat = data['latitude']
    user_long = data['longitude']
    photo_base64 = data['photo']  # Data image base64 dari Web Camera

    # 1. Validasi Geofencing
    is_inside, distance = GeofencingVerifier.verify_presence(user_lat, user_long, OFFICE_LAT, OFFICE_LONG)
    if not is_inside:
        return jsonify({
            "status": "rejected", 
            "message": f"Anda berada di luar radius kantor ({round(distance, 2)} meter dari koordinat)."
        }), 403

    # 2. Logika Penentuan Terlambat (Contoh batas jam 08:00 AM)
    now = datetime.now()
    status = "HADIR"
    if now.hour >= 8:
        status = "TERLAMBAT"

    # 3. Simpan Transaksi ke PostgreSQL
    new_attendance = Attendance(
        employee_id=uuid.UUID(current_user_id),
        check_in_time=now,
        check_in_lat=user_lat,
        check_in_long=user_long,
        photo_in_url="cloud_storage_mock_path.png",  # Implementasikan upload cloud storage di service layer
        status=status
    )
    
    db.session.add(new_attendance)
    db.session.commit()

    return jsonify({
        "status": "success",
        "message": "Absensi berhasil dicatat!",
        "data": {
            "status_kehadiran": status,
            "waktu": now.strftime("%Y-%m-%d %H:%M:%S")
        }
    }), 200