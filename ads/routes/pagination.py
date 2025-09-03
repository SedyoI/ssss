from flask import jsonify, request
from ads import ads_bp
from ads.models import Ad
from ads.utils import format_ad_response

@ads_bp.route('/ads', methods=['GET'])
def get_all_ads():
    try:
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=5, type=int)

        if page < 1 or per_page < 1:
            return jsonify({"error": "Параметри 'page' і 'per_page' повинні бути більшими за 0."}), 400

        paginated_ads = Ad.query.paginate(page=page, per_page=per_page, error_out=False)

        if not paginated_ads.items:
            return jsonify({"message": "Оголошення не знайдені."}), 404

        results = [
            format_ad_response(ad, [image.image_url for image in ad.images])
            for ad in paginated_ads.items
        ]

        return jsonify({
            "message": "Це головна сторінка з оголошеннями.",
            "data": results,
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total": paginated_ads.total,
                "pages": paginated_ads.pages
            }
        }), 200

    except Exception as e:
        return jsonify({"error": f"Виникла помилка: {str(e)}"}), 500

