from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ads import ads_bp
from ads.models import UserRating, Ad
from ads.utils import format_rating_response
import requests
from sqlalchemy.exc import IntegrityError

@ads_bp.route('/users/<user_id>/ratings', methods=['GET'])
def get_user_ratings(user_id):
    """Отримати всі рейтинги користувача."""
    try:
        # Отримати рейтинги з пагінацією
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=10, type=int)

        ratings_query = UserRating.query.filter_by(rated_user_id=user_id).order_by(UserRating.created_at.desc())
        paginated_ratings = ratings_query.paginate(page=page, per_page=per_page, error_out=False)

        # Форматувати рейтинги
        ratings_data = []
        for rating in paginated_ratings.items:
            # Отримати email користувача, який поставив оцінку
            try:
                user_email_url = f"http://localhost:8077/api/user/{rating.rater_user_id}/email"
                response = requests.get(user_email_url)
                rater_email = response.json().get("email", "Невідомий користувач") if response.status_code == 200 else "Невідомий користувач"
            except:
                rater_email = "Невідомий користувач"

            rating_data = format_rating_response(rating, rater_email)
            ratings_data.append(rating_data)

        # Отримати статистику рейтингу
        average_rating = UserRating.get_user_average_rating(user_id)
        ratings_count = UserRating.get_user_ratings_count(user_id)

        return jsonify({
            "message": "Рейтинги отримано успішно.",
            "data": ratings_data,
            "statistics": {
                "average_rating": average_rating,
                "total_ratings": ratings_count
            },
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total": paginated_ratings.total,
                "pages": paginated_ratings.pages
            }
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@ads_bp.route('/ads/<int:ad_id>/rate', methods=['POST'])
@jwt_required()
def rate_user(ad_id):
    """Поставити оцінку користувачу за оголошення."""
    try:
        # Отримати user_id з JWT
        rater_user_id = get_jwt_identity()
        if not rater_user_id:
            return jsonify({"error": "Не вдалося отримати userId з токену."}), 400

        # Перевірити, чи існує оголошення
        ad = Ad.find_by_id(ad_id)
        if not ad:
            return jsonify({"error": "Оголошення не знайдено."}), 404

        # Отримати дані з запиту
        data = request.get_json()
        if not data or 'rating' not in data:
            return jsonify({"error": "Рейтинг обов'язковий."}), 400

        rating_value = data['rating']
        comment = data.get('comment', '').strip()
        rated_user_id = ad.user_id  # Оцінюємо автора оголошення

        # Перевірити, чи користувач не намагається оцінити сам себе
        if rater_user_id == rated_user_id:
            return jsonify({"error": "Ви не можете оцінити самого себе."}), 400

        # Перевірити, чи користувач вже оцінював це оголошення
        existing_rating = UserRating.query.filter_by(
            rated_user_id=rated_user_id,
            rater_user_id=rater_user_id,
            ad_id=ad_id
        ).first()

        if existing_rating:
            # Оновити існуючий рейтинг
            existing_rating.update(rating_value, comment if comment else None)
            
            # Отримати email користувача для відповіді
            try:
                user_email_url = f"http://localhost:8077/api/user/{rater_user_id}/email"
                response = requests.get(user_email_url)
                rater_email = response.json().get("email", "Невідомий користувач") if response.status_code == 200 else "Невідомий користувач"
            except:
                rater_email = "Невідомий користувач"

            rating_data = format_rating_response(existing_rating, rater_email)
            
            return jsonify({
                "message": "Рейтинг оновлено успішно.",
                "data": rating_data
            }), 200
        else:
            # Створити новий рейтинг
            new_rating = UserRating(
                rated_user_id=rated_user_id,
                rater_user_id=rater_user_id,
                ad_id=ad_id,
                rating=rating_value,
                comment=comment if comment else None
            )
            new_rating.save()

            # Отримати email користувача для відповіді
            try:
                user_email_url = f"http://localhost:8077/api/user/{rater_user_id}/email"
                response = requests.get(user_email_url)
                rater_email = response.json().get("email", "Невідомий користувач") if response.status_code == 200 else "Невідомий користувач"
            except:
                rater_email = "Невідомий користувач"

            rating_data = format_rating_response(new_rating, rater_email)

            return jsonify({
                "message": "Рейтинг додано успішно.",
                "data": rating_data
            }), 201

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except IntegrityError:
        return jsonify({"error": "Ви вже оцінили цього користувача за це оголошення."}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@ads_bp.route('/ratings/<int:rating_id>', methods=['DELETE'])
@jwt_required()
def delete_rating(rating_id):
    """Видалити рейтинг."""
    try:
        # Отримати user_id з JWT
        user_id = get_jwt_identity()
        if not user_id:
            return jsonify({"error": "Не вдалося отримати userId з токену."}), 400

        # Знайти рейтинг
        rating = UserRating.find_by_id(rating_id)
        if not rating:
            return jsonify({"error": "Рейтинг не знайдено."}), 404

        # Перевірити права доступу (користувач може видаляти тільки свої рейтинги)
        if rating.rater_user_id != user_id:
            return jsonify({"error": "Ви можете видаляти тільки свої рейтинги."}), 403

        # Видалити рейтинг
        rating.delete()

        return jsonify({"message": "Рейтинг видалено успішно."}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@ads_bp.route('/users/<user_id>/rating-summary', methods=['GET'])
def get_user_rating_summary(user_id):
    """Отримати короткий підсумок рейтингу користувача."""
    try:
        average_rating = UserRating.get_user_average_rating(user_id)
        ratings_count = UserRating.get_user_ratings_count(user_id)

        # Розподіл оцінок
        rating_distribution = {}
        for i in range(1, 6):
            count = UserRating.query.filter_by(rated_user_id=user_id, rating=i).count()
            rating_distribution[str(i)] = count

        return jsonify({
            "user_id": user_id,
            "average_rating": average_rating,
            "total_ratings": ratings_count,
            "rating_distribution": rating_distribution
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500