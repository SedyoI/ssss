from flask import request, jsonify, current_app
from werkzeug.utils import secure_filename
from flask_jwt_extended import jwt_required, get_jwt_identity
import os
import requests  # Додано для HTTP-запитів
from ads import ads_bp  # Імпортуємо існуючий блупрінт
from ads.models import Ad, AdImage
from ads.utils import allowed_file, format_ad_response
from ads.agrotracker_sendgrind import send_notification_email

@ads_bp.route('/add', methods=['POST'])
@jwt_required() 
def add_ad_with_images():
    data = request.form.to_dict()
    print("DATA:", data)
    files = request.files.getlist('images')

    if len(files) > 7:
        return jsonify({"error": "Максимальна кількість зображень - 7."}), 400

    try:
        # Витягування userId із JWT-токену
        user_id = get_jwt_identity()

        if not user_id:
            return jsonify({"error": "Не вдалося отримати userId з токену."}), 400

        # Отримання email через API-запит
        user_email_url = f"http://localhost:8077/api/user/{user_id}/email"
        response = requests.get(user_email_url)
        if response.status_code != 200:
            return jsonify({"error": "Не вдалося отримати email користувача."}), 400

        user_email = response.json().get("email")
        if not user_email:
            return jsonify({"error": "Email користувача відсутній у відповіді API."}), 400

        # Перетворення ціни у число (якщо є)
        if 'price' in data:
            data['price'] = float(data['price'])

        # Збереження оголошення
        ad = Ad(**data, user_id=user_id)  # user_id передається в модель
        ad.save()

        # Завантаження зображень
        uploaded_images = []
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                image_url = f'/uploads/{filename}'
                ad_image = AdImage(ad_id=ad.id, image_url=image_url)
                ad_image.save()
                uploaded_images.append(image_url)

        # Надсилання email-сповіщення
        send_notification_email(
            to_email=user_email,
            subject="Ваша заявка успішно створена!",
            message=f"""
            Шановний користувачу,
            Ваша заявка {ad.title} була успішно створена!
            Опис: {ad.description}
            Локація: {ad.location}
            Ціна: {ad.price} UAH
            Дякуємо за використання нашого сервісу AgroTracker!
            Очікуйте повідомлення, якщо хтось обере вашу заявку
            """
        )

        # Форматування відповіді
        response_data = format_ad_response(ad, images=uploaded_images)
        return jsonify({"message": "Заявка успішно створена.", "data": response_data}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400
