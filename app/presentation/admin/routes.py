from flask import Blueprint, request, jsonify, render_template
from app.data.models import db, Employee, Role, Attendance, LeaveRequest
import uuid
from datetime import date

# Blueprint untuk Admin/HRD
admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/api/v1/admin/add-employee', methods=['POST'])
def add_employee():
    data = request.get_json()
    
    role_karyawan = Role.query.filter_by(name='Karyawan').first()
    if not role_karyawan:
        return jsonify({"status": "error", "message": "Role 'Karyawan' belum ada di database!"}), 400

    existing_emp = Employee.query.filter((Employee.email == data['email']) | (Employee.nik == data['nik'])).first()
    if existing_emp:
        return jsonify({"status": "error", "message": "Gagal! Email atau NIK tersebut sudah terdaftar."}), 400
    
    new_emp = Employee(
        id=uuid.uuid4(),
        nik=data['nik'],
        email=data['email'],
        password_hash=data['password'],
        full_name=data['full_name'],
        role_id=role_karyawan.id,
        position=data.get('position', 'Staff'),
        department=data.get('department', 'General')
    )
    
    db.session.add(new_emp)
    db.session.commit()
    
    return jsonify({"status": "success", "message": f"Karyawan {data['full_name']} berhasil didaftarkan!"}), 201

# --- STATISTIK REAL-TIME HRD ---
@admin_bp.route('/api/v1/admin/realtime-stats', methods=['GET'])
def get_realtime_stats():
    today = date.today()
    
    role_karyawan = Role.query.filter_by(name='Karyawan').first()
    role_id_karyawan = role_karyawan.id if role_karyawan else 2
    
    total_karyawan = Employee.query.filter_by(role_id=role_id_karyawan).count()
    hadir = Attendance.query.filter(db.func.date(Attendance.check_in_time) == today).count()
    
    izin_cuti = LeaveRequest.query.filter(
        LeaveRequest.start_date <= today, 
        LeaveRequest.end_date >= today, 
        LeaveRequest.status == 'APPROVED'
    ).count()
    
    alfa = total_karyawan - (hadir + izin_cuti)
    if alfa < 0: 
        alfa = 0 
        
    pending_cuti = LeaveRequest.query.filter_by(status='PENDING').count()

    return jsonify({
        "total_karyawan": total_karyawan,
        "hadir": hadir,
        "izin_cuti": izin_cuti,
        "alfa": alfa,
        "pending_cuti": pending_cuti
    })

# --- RUTE HALAMAN UI ADMIN ---
@admin_bp.route('/approval', methods=['GET'])
def approval_page():
    return render_template('approval.html')

@admin_bp.route('/payroll-admin', methods=['GET'])
def payroll_admin_page():
    return render_template('payroll.html')

# --- API PERSETUJUAN CUTI ---
@admin_bp.route('/api/v1/admin/leaves/pending', methods=['GET'])
def get_pending_leaves():
    leaves = LeaveRequest.query.filter_by(status='PENDING').all()
    
    data = []
    for leave in leaves:
        emp = Employee.query.get(leave.employee_id) 
        data.append({
            "id": str(leave.id), # UUID diubah ke string agar aman dikirim via JSON
            "employee_name": emp.full_name if emp else "Tidak Diketahui",
            "reason": leave.reason,
            "start_date": leave.start_date.strftime("%d %b %Y"),
            "end_date": leave.end_date.strftime("%d %b %Y")
        })
        
    return jsonify(data)

@admin_bp.route('/api/v1/admin/leave/<string:leave_id>', methods=['PUT'])
def update_leave_status(leave_id):
    data = request.get_json()
    new_status = data.get('status')
    
    leave = LeaveRequest.query.get(leave_id)
    if not leave:
        return jsonify({"message": "Data cuti tidak ditemukan"}), 404
        
    leave.status = new_status
    db.session.commit()
    
    return jsonify({"message": f"Status cuti berhasil diubah menjadi {new_status}"})

# --- API UNTUK MENGAMBIL DATA KARYAWAN DI PAYROLL (DISEMPURNAKAN) ---
@admin_bp.route('/api/v1/admin/payroll-list', methods=['GET'])
def get_payroll_list():
    try:
        # Coba ambil semua karyawan dari database tanpa batasan role yang ketat
        employees = Employee.query.all()
        
        data = []
        for emp in employees:
            # Lewatkan akun yang mungkin berstatus admin/HRD jika ingin murni karyawan, 
            # Tapi jika ingin menampilkan semuanya, biarkan baris ini aktif:
            data.append({
                "id": str(emp.id),
                "full_name": emp.full_name,
                "nik": emp.nik,
                "position": emp.position or "Staff"
            })
            
        return jsonify(data), 200
    except Exception as e:
        print("Error payroll list:", str(e))
        return jsonify({"error": str(e)}), 500