from flask import jsonify, current_app
from ads import ads_bp
from ads.models import Ad, AdImage
import os

@ads_bp.route('/delete/<int:ad_id>', methods=['POST'])
def delete_ad(ad_id):
    # Знайти заявку
    ad = Ad.find_by_id(ad_id)
    if not ad:
        return jsonify({"error": "Ad not found"}), 404

    try:
        # Отримати всі зображення заявки
        images = AdImage.query.filter_by(ad_id=ad_id).all()

        # Видалити файли зображень із диска
        for image in images:
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], os.path.basename(image.image_url))
            if os.path.exists(file_path):
                os.remove(file_path)
            # Видалити запис про зображення з бази даних
            image.delete()

        # Видалити заявку
        ad.delete()

        return jsonify({"message": f"Ad with ID {ad_id} and its images were deleted"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400
