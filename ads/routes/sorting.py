from flask import request, jsonify
from ads import ads_bp
from ads.models import Ad
from ads.utils import format_ad_response

@ads_bp.route('/sort', methods=['GET'])
def sort_ads():
    try:
        # Отримуємо параметр для сортування, якщо є
        sort = request.args.get('sort_by_price', '').strip().lower()

        # Створюємо базовий запит
        query = Ad.query

        # Перевіряємо, чи є параметр сортування, і застосовуємо відповідне сортування
        if sort == 'asc':
            query = query.order_by(Ad.price.asc())
        elif sort == 'desc':
            query = query.order_by(Ad.price.desc())
        elif sort != '':
            # Якщо значення сортування не 'asc' або 'desc', можемо повернути помилку
            return jsonify({"error": "Невірний параметр сортування. Використовуйте 'asc' або 'desc'."}), 400

        # Отримуємо всі оголошення після сортування
        ads = query.all()

        # Перевіряємо наявність оголошень
        if not ads:
            return jsonify({"message": "Оголошення не знайдені."}), 404
        # Формування результатів
        results = []
        for ad in ads:
            # Отримання URL зображень для кожного оголошення
            images = [image.image_url for image in ad.images]
            # Форматування оголошення
            ad_response = format_ad_response(ad, images)
            results.append(ad_response)

        # Повернення результатів
        return jsonify({"message": "Результати пошуку:", "data": results}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400
