from flask import request, jsonify
from ads import ads_bp
from ads.models import Ad
from ads.utils import format_ad_response


@ads_bp.route('/filter', methods=['GET'])
def filter_ads():
    """
    Функція для фільтрації оголошень за location, region та district.
    """
    try:
        # Отримання параметрів фільтрації
        location = request.args.get('location', '').lower()

        # Базовий запит для фільтрації
        query = Ad.query

        # Додавання умов залежно від параметрів
        if location:
            query = query.filter(Ad.location.ilike(f"%{location}%"))
        # Виконання запиту
        ads = query.all()

        # Якщо оголошення не знайдено
        if not ads:
            return jsonify({"message": "Оголошення не знайдені."}), 404

        # Формування результатів
        results = []
        for ad in ads:
            # Отримання URL зображень для оголошення
            images = [image.image_url for image in ad.images]
            # Форматування відповіді
            ad_response = format_ad_response(ad, images)
            results.append(ad_response)

        return jsonify({"message": "Результати фільтрації:", "data": results}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400
