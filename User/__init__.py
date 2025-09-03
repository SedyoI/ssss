from flask import Blueprint

user_bp = Blueprint('user', __name__, url_prefix='/user')

from User.routes import profile
#from User.routes import edit  # Додаємо новий маршрут

# Реєструємо маршрути
user_bp.register_blueprint(profile.profile_bp)
#user_bp.register_blueprint(edit.edit_bp)
