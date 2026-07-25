import os
from flask import Flask
from flask_jwt_extended import JWTManager
from app.data.models import db
from datetime import timedelta

def create_app():
    # Arahkan Flask untuk mencari ke dalam folder 'presentation/templates'
    base_dir = os.path.abspath(os.path.dirname(__file__))
    template_dir = os.path.join(base_dir, 'presentation', 'templates')
    
    app = Flask(__name__, template_folder=template_dir, static_folder='static')
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin123@localhost:5432/hris_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    app.config['SECRET_KEY'] = 'super-secret-premium-key-2026'
    app.config['JWT_SECRET_KEY'] = 'jwt-secret-hris-2026'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=8)
    
    db.init_app(app)
    jwt = JWTManager(app)
    
    # Import Blueprints
    from app.presentation.auth.routes import auth_bp
    from app.presentation.dashboard.routes import dashboard_bp
    from app.presentation.attendance.routes import attendance_bp
    from app.presentation.leave.routes import leave_bp
    from app.presentation.profile.routes import profile_bp
    from app.presentation.payroll.routes import payroll_bp
    from app.presentation.report.routes import report_bp
    from app.presentation.announcement.routes import announcement_bp
    from app.presentation.settings.routes import settings_bp
    
    # --- TAMBAHAN BARU: Import Admin Blueprint Anda ---
    from app.presentation.admin.routes import admin_bp
    
    # Register Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(attendance_bp)
    app.register_blueprint(leave_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(payroll_bp)
    app.register_blueprint(report_bp)
    app.register_blueprint(announcement_bp)
    app.register_blueprint(settings_bp)
    
    # --- TAMBAHAN BARU: Daftarkan Admin Blueprint ke Flask ---
    app.register_blueprint(admin_bp)
    
    with app.app_context():
        db.create_all()
        
    return app