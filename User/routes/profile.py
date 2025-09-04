from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
import requests
from ads.utils import format_ad_response
from ads.models import Ad
from ads.models import UserRating
#from User.models import User  # Модель User із зовнішнього сервісу

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    try:
        # Отримуємо `user_id` із JWT
        current_user_id = get_jwt_identity()
        if not current_user_id:
            return jsonify({"error": "Не вдалося отримати userId з токену."}), 400

        # Отримання email через API-запит
        #user_email_url = f"http://localhost:8077/api/user/{current_user_id}/email"
        #response = requests.get(user_email_url)
        #if response.status_code != 200:
         #   return jsonify({"error": "Не вдалося отримати email користувача."}), 400

        #user_email = response.json().get("email")
        #if not user_email:
         #   return jsonify({"error": "Email користувача відсутній у відповіді API."}), 400

        # Отримання оголошень для цього користувача
        ads = Ad.query.filter_by(user_id=current_user_id).all()
        ads_data = [
            format_ad_response(ad, [image.image_url for image in ad.images])
            for ad in ads
        ]

        # Отримання статистики рейтингу користувача
        average_rating = UserRating.get_user_average_rating(current_user_id)
        ratings_count = UserRating.get_user_ratings_count(current_user_id)
        # Підготовка відповіді
        user_data = {
           # "user_id": current_user_id,
            #"email": user_email,
            "ads": ads_data,
            "rating_info": {
                "average_rating": average_rating,
                "total_ratings": ratings_count
            }
        }
        return jsonify(user_data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
