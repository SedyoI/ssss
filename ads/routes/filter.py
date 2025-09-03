from flask import request, jsonify
from ads import ads_bp
from ads.models import Ad
from ads.utils import format_ad_response


@ads_bp.route('/filter', methods=['GET'])
def filter_ads():
    """
    Функція для фільтрації оголошень за location.
    """
    try:
        # Отримання параметрів фільтрації
        location = request.args.get('location', '').lower()
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=10, type=int)

        # Базовий запит для фільтрації
        query = Ad.query

        # Додавання умов залежно від параметрів
        if location:
            query = query.filter(Ad.location.ilike(f"%{location}%"))
        
        # Виконання запиту
        paginated_ads = query.paginate(page=page, per_page=per_page, error_out=False)

        # Якщо оголошення не знайдено
        if not paginated_ads.items:
            return jsonify({"message": "Оголошення не знайдені."}), 404

        # Формування результатів
        results = []
        for ad in paginated_ads.items:
            # Отримання URL зображень для оголошення
            images = [image.image_url for image in ad.images]
            # Форматування відповіді
            ad_response = format_ad_response(ad, images)
            results.append(ad_response)

        return jsonify({
            "message": "Результати фільтрації:", 
            "data": results,
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total": paginated_ads.total,
                "pages": paginated_ads.pages
            }
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400
