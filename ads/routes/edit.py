from flask import request, jsonify, current_app
import os
from werkzeug.utils import secure_filename
from ads import ads_bp
from ads.models import Ad, AdImage
from ads.utils import allowed_file, format_ad_response

@ads_bp.route('/edit/<int:ad_id>', methods=['PUT'])
def edit_ad(ad_id):
    """
    Редагувати заявку з можливістю додавання або видалення зображень.
    """
    # Отримуємо заявку
    ad = Ad.find_by_id(ad_id)
    if not ad:
        return jsonify({"error": "Ad not found"}), 404

    # Дані для оновлення заявки
    data = request.form.to_dict()

    # Отримуємо список файлів із форми
    files = request.files.getlist('images')

    # Отримуємо список зображень для видалення (ID)
    delete_image_ids = request.form.getlist('delete_images')  # Наприклад, ['1', '2', ...]

    try:
        # Оновлення даних заявки
        ad.update(data)

        # Видалення зазначених зображень
        if delete_image_ids:
            for image_id in delete_image_ids:
                image = AdImage.find_by_id(image_id)
                if image and image.ad_id == ad_id:
                    # Видаляємо файл із диска
                    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], os.path.basename(image.image_url))
                    if os.path.exists(file_path):
                        os.remove(file_path)
                    # Видаляємо запис із бази даних
                    image.delete()

        # Додавання нових зображень
        if files:
            existing_images_count = len(ad.images)  # Кількість уже існуючих зображень
            if existing_images_count + len(files) > 7:
                return jsonify({"error": "Загальна кількість зображень не може перевищувати 7."}), 400

            for file in files:
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                    file.save(file_path)

                    # Додаємо URL зображення в базу даних
                    image_url = f'/uploads/{filename}'
                    ad_image = AdImage(ad_id=ad.id, image_url=image_url)
                    ad_image.save()

        response_data = format_ad_response(ad, images=[image.image_url for image in ad.images])
        return jsonify({"message": "Заявка успішно оновлена.", "data": response_data}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400