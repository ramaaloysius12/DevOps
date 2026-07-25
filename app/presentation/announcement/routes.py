from flask import Blueprint, render_template, jsonify, request
from app.data.models import db, Announcement

announcement_bp = Blueprint('announcement', __name__, template_folder='../../templates')

@announcement_bp.route('/announcement', methods=['GET'])
def announcement_page():
    return render_template('announcement.html')

@announcement_bp.route('/api/v1/announcements', methods=['GET'])
def get_announcements():
    # Mengambil semua pengumuman diurutkan dari yang terbaru
    posts = Announcement.query.order_by(Announcement.created_at.desc()).all()
    return jsonify([{
        "title": p.title, 
        "content": p.content, 
        "created_at": p.created_at
    } for p in posts])

# --- TAMBAHAN BARU: Endpoint untuk menerima data dari Dashboard HRD ---
@announcement_bp.route('/api/v1/announcement', methods=['POST'])
def create_announcement():
    data = request.get_json()
    
    # Validasi apakah judul dan isi kosong
    if not data or not data.get('title') or not data.get('content'):
        return jsonify({"status": "error", "message": "Judul dan isi harus diisi"}), 400
    
    # Simpan ke tabel Announcement di database
    new_announcement = Announcement(
        title=data['title'],
        content=data['content']
    )
    db.session.add(new_announcement)
    db.session.commit()
    
    return jsonify({"status": "success", "message": "Pengumuman berhasil diposting"}), 201