from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ads import ads_bp
from ads.models import Comment, Ad
from ads.utils import format_comment_response
import requests

@ads_bp.route('/ads/<int:ad_id>/comments', methods=['GET'])
def get_comments(ad_id):
    """Отримати всі коментарі до оголошення."""
    try:
        # Перевірити, чи існує оголошення
        ad = Ad.find_by_id(ad_id)
        if not ad:
            return jsonify({"error": "Оголошення не знайдено."}), 404

        # Отримати коментарі з пагінацією
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=10, type=int)

        comments_query = Comment.query.filter_by(ad_id=ad_id).order_by(Comment.created_at.desc())
        paginated_comments = comments_query.paginate(page=page, per_page=per_page, error_out=False)

        # Форматувати коментарі
        comments_data = []
        for comment in paginated_comments.items:
            # Отримати email користувача через API
            try:
                user_email_url = f"http://localhost:8077/api/user/{comment.user_id}/email"
                response = requests.get(user_email_url)
                user_email = response.json().get("email", "Невідомий користувач") if response.status_code == 200 else "Невідомий користувач"
            except:
                user_email = "Невідомий користувач"

            comment_data = format_comment_response(comment, user_email)
            comments_data.append(comment_data)

        return jsonify({
            "message": "Коментарі отримано успішно.",
            "data": comments_data,
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total": paginated_comments.total,
                "pages": paginated_comments.pages
            }
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@ads_bp.route('/ads/<int:ad_id>/comments', methods=['POST'])
@jwt_required()
def add_comment(ad_id):
    """Додати коментар до оголошення."""
    try:
        # Отримати user_id з JWT
        user_id = get_jwt_identity()
        if not user_id:
            return jsonify({"error": "Не вдалося отримати userId з токену."}), 400

        # Перевірити, чи існує оголошення
        ad = Ad.find_by_id(ad_id)
        if not ad:
            return jsonify({"error": "Оголошення не знайдено."}), 404

        # Отримати дані з запиту
        data = request.get_json()
        if not data or 'content' not in data:
            return jsonify({"error": "Контент коментаря обов'язковий."}), 400

        content = data['content'].strip()
        if not content:
            return jsonify({"error": "Коментар не може бути порожнім."}), 400

        # Створити коментар
        comment = Comment(
            ad_id=ad_id,
            user_id=user_id,
            content=content
        )
        comment.save()

        # Отримати email користувача для відповіді
        try:
            user_email_url = f"http://localhost:8077/api/user/{user_id}/email"
            response = requests.get(user_email_url)
            user_email = response.json().get("email", "Невідомий користувач") if response.status_code == 200 else "Невідомий користувач"
        except:
            user_email = "Невідомий користувач"

        # Форматувати відповідь
        comment_data = format_comment_response(comment, user_email)

        return jsonify({
            "message": "Коментар додано успішно.",
            "data": comment_data
        }), 201

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@ads_bp.route('/comments/<int:comment_id>', methods=['PUT'])
@jwt_required()
def update_comment(comment_id):
    """Оновити коментар."""
    try:
        # Отримати user_id з JWT
        user_id = get_jwt_identity()
        if not user_id:
            return jsonify({"error": "Не вдалося отримати userId з токену."}), 400

        # Знайти коментар
        comment = Comment.find_by_id(comment_id)
        if not comment:
            return jsonify({"error": "Коментар не знайдено."}), 404

        # Перевірити права доступу
        if comment.user_id != user_id:
            return jsonify({"error": "Ви можете редагувати тільки свої коментарі."}), 403

        # Отримати нові дані
        data = request.get_json()
        if not data or 'content' not in data:
            return jsonify({"error": "Контент коментаря обов'язковий."}), 400

        content = data['content'].strip()
        if not content:
            return jsonify({"error": "Коментар не може бути порожнім."}), 400

        # Оновити коментар
        comment.update(content)

        # Отримати email користувача для відповіді
        try:
            user_email_url = f"http://localhost:8077/api/user/{user_id}/email"
            response = requests.get(user_email_url)
            user_email = response.json().get("email", "Невідомий користувач") if response.status_code == 200 else "Невідомий користувач"
        except:
            user_email = "Невідомий користувач"

        # Форматувати відповідь
        comment_data = format_comment_response(comment, user_email)

        return jsonify({
            "message": "Коментар оновлено успішно.",
            "data": comment_data
        }), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@ads_bp.route('/comments/<int:comment_id>', methods=['DELETE'])
@jwt_required()
def delete_comment(comment_id):
    """Видалити коментар."""
    try:
        # Отримати user_id з JWT
        user_id = get_jwt_identity()
        if not user_id:
            return jsonify({"error": "Не вдалося отримати userId з токену."}), 400

        # Знайти коментар
        comment = Comment.find_by_id(comment_id)
        if not comment:
            return jsonify({"error": "Коментар не знайдено."}), 404

        # Перевірити права доступу (користувач може видаляти тільки свої коментарі)
        if comment.user_id != user_id:
            return jsonify({"error": "Ви можете видаляти тільки свої коментарі."}), 403

        # Видалити коментар
        comment.delete()

        return jsonify({"message": "Коментар видалено успішно."}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500