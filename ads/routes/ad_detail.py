from flask import render_template, jsonify
from ads import ads_bp
from ads.models import Ad
import requests

@ads_bp.route('/ad/<int:ad_id>', methods=['GET'])
def get_ad_detail(ad_id):
    """Отримати детальну інформацію про оголошення."""
    try:
        # Знайти оголошення
        ad = Ad.find_by_id(ad_id)
        if not ad:
            return jsonify({"error": "Оголошення не знайдено."}), 404

        # Отримати email автора оголошення
        try:
            user_email_url = f"http://localhost:8077/api/user/{ad.user_id}/email"
            response = requests.get(user_email_url)
            seller_email = response.json().get("email", "Невідомий користувач") if response.status_code == 200 else "Невідомий користувач"
        except:
            seller_email = "Невідомий користувач"

        # Рендерити HTML сторінку
        return render_template('ad_detail.html', ad=ad, seller_email=seller_email)

    except Exception as e:
        return jsonify({"error": str(e)}), 500