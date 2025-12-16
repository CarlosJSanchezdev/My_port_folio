from flask import Blueprint, send_from_directory, session, jsonify, current_app
import os

bp = Blueprint('protected', __name__)

@bp.route('/cv', methods=['GET'])
def get_cv():
    """Serves the CV only to authenticated users with Level 3 access"""
    # Check authentication
    if not session.get('user_id'):
        return jsonify({'error': 'Unauthorized', 'message': 'Please logging in.'}), 401
    
    # Check access level
    access_level = session.get('access_level', 1)
    if access_level < 3:
        return jsonify({'error': 'Forbidden', 'message': 'Insufficient access level.'}), 403

    # Define path
    # Assuming backend runs from root or we use current_app.root_path
    # We moved file to backend/protected_assets/cv_cjs.pdf
    # The app is created in backend/app/__init__.py, so root_path is likely backend/app
    # We want backend/protected_assets which is sibling to app
    
    protected_dir = os.path.join(current_app.root_path, '..', 'protected_assets')
    protected_dir = os.path.abspath(protected_dir)

    try:
        return send_from_directory(protected_dir, 'cv_cjs.pdf', as_attachment=True)
    except FileNotFoundError:
        return jsonify({'error': 'Not Found', 'message': 'The requested file was not found on the server.'}), 404
