def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def format_ad_response(ad, images=None):
   
    return {
        "id": ad.id,
        "title": ad.title,
        "description": ad.description,
        "location": ad.location,
        "price": ad.price,
        "images": images or [],
        "user_id": ad.user_id,
        "created_at": ad.created_at.isoformat() if ad.created_at else None,
        "comments_count": len(ad.comments) if ad.comments else 0
    }

def format_comment_response(comment, user_email=None):
    """Форматувати відповідь для коментаря."""
    return {
        "id": comment.id,
        "ad_id": comment.ad_id,
        "user_id": comment.user_id,
        "user_email": user_email,
        "content": comment.content,
        "created_at": comment.created_at.isoformat(),
        "updated_at": comment.updated_at.isoformat()
    }

def format_rating_response(rating, rater_email=None):
    """Форматувати відповідь для рейтингу."""
    return {
        "id": rating.id,
        "rated_user_id": rating.rated_user_id,
        "rater_user_id": rating.rater_user_id,
        "rater_email": rater_email,
        "ad_id": rating.ad_id,
        "rating": rating.rating,
        "comment": rating.comment,
        "created_at": rating.created_at.isoformat(),
        "updated_at": rating.updated_at.isoformat()
    }