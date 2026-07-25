from flask import Blueprint, render_template

settings_bp = Blueprint('settings', __name__, template_folder='../../templates')

@settings_bp.route('/settings', methods=['GET'])
def settings_page():
    return render_template('settings.html')