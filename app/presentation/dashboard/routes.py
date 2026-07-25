from flask import Blueprint, render_template
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.data.models import Employee, Attendance
from datetime import datetime
from app.data.models import Employee, Attendance, LeaveRequest

dashboard_bp = Blueprint('dashboard', __name__, template_folder='../../templates')

# Dalam praktiknya, render_template untuk dashboard bisa menggunakan template standar,
# sedangkan datanya diambil secara asinkron via API endpoint lain. 
# Untuk mempermudah, kita satukan validasi tampilan di sini.

@dashboard_bp.route('/dashboard-hrd', methods=['GET'])
def dashboard_hrd_page():
    # Mengambil statistik dari database
    total_karyawan = Employee.query.count()
    total_hadir = Attendance.query.filter_by(status='HADIR').count()
    pending_cuti = LeaveRequest.query.filter_by(status='PENDING').count()
    
    stats = {
        "total_karyawan": total_karyawan,
        "total_hadir": total_hadir,
        "pending_cuti": pending_cuti
    }
    return render_template('dashboard_hrd.html', stats=stats)

@dashboard_bp.route('/dashboard', methods=['GET'])
def dashboard_page():
    # Catatan: Jika menggunakan arsitektur SPA/AJAX, biarkan endpoint ini terbuka
    # lalu validasi JWT di sisi Client (JavaScript) sebelum memuat data.
    
    # Mock data statistik (Di production, lakukan query COUNT ke SQLAlchemy)
    stats = {
        "total_karyawan": 150,
        "hadir_hari_ini": 142,
        "terlambat": 5,
        "cuti_alpha": 3
    }
    
    return render_template('dashboard.html', stats=stats)
