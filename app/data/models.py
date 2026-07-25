# app/data/models.py
import uuid
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID

db = SQLAlchemy()

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    employees = db.relationship('Employee', backref='role', lazy=True)

class Employee(db.Model):
    __tablename__ = 'employees'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nik = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(150), nullable=False)
    position = db.Column(db.String(100), nullable=True, default='Staff')
    department = db.Column(db.String(100), nullable=True, default='General')
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relasi ke tabel lain
    attendances = db.relationship('Attendance', backref='employee', lazy=True)
    leaves = db.relationship('LeaveRequest', backref='employee', lazy=True)
    payrolls = db.relationship('Payroll', backref='employee', lazy=True)
    reports = db.relationship('WorkReport', backref='employee', lazy=True)

class Attendance(db.Model):
    __tablename__ = 'attendances'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    employee_id = db.Column(UUID(as_uuid=True), db.ForeignKey('employees.id', ondelete='CASCADE'), nullable=False)
    check_in_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    check_out_time = db.Column(db.DateTime, nullable=True)
    check_in_lat = db.Column(db.Numeric(10, 8), nullable=False)
    check_in_long = db.Column(db.Numeric(11, 8), nullable=False)
    photo_in_url = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(20), nullable=False, default='HADIR')

class LeaveRequest(db.Model):
    __tablename__ = 'leave_requests'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    employee_id = db.Column(UUID(as_uuid=True), db.ForeignKey('employees.id', ondelete='CASCADE'), nullable=False)
    leave_type = db.Column(db.String(50), nullable=False) # TAHUNAN, SAKIT, PRIBADI
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    reason = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='PENDING') # PENDING, APPROVED, REJECTED
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Payroll(db.Model):
    __tablename__ = 'payrolls'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    employee_id = db.Column(UUID(as_uuid=True), db.ForeignKey('employees.id', ondelete='CASCADE'), nullable=False)
    month_year = db.Column(db.String(20), nullable=False) # Contoh: "Agustus 2026"
    basic_salary = db.Column(db.Numeric(12, 2), nullable=False)
    allowance = db.Column(db.Numeric(12, 2), default=0)
    deduction = db.Column(db.Numeric(12, 2), default=0)
    net_salary = db.Column(db.Numeric(12, 2), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class WorkReport(db.Model):
    __tablename__ = 'work_reports'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    employee_id = db.Column(UUID(as_uuid=True), db.ForeignKey('employees.id', ondelete='CASCADE'), nullable=False)
    report_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='SUBMITTED')

class Announcement(db.Model):
    __tablename__ = 'announcements'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
