from app import db
from sqlalchemy.orm import validates
from datetime import datetime

MAX_PRICE = 1000000.0  # максимальна ціна
MIN_PRICE = 0.0  # мінімальна ціна
MAX_DESCRIPTION_LENGTH = 1000  # максимальна кількість символів для опису
MAX_TITLE_LENGTH = 100
MAX_LOCATION_LENGTH = 100
MAX_URL_LENGTH = 255
MAX_COMMENT_LENGTH = 500


class Ad(db.Model):
    """Модель оголошення."""
    __tablename__ = 'ads'

    id = db.Column(db.Integer, primary_key=True)
    #email = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(MAX_TITLE_LENGTH), nullable=False)
    description = db.Column(db.String(MAX_DESCRIPTION_LENGTH), nullable=False)
    price = db.Column(db.Float, nullable=False)
    location = db.Column(db.String(MAX_LOCATION_LENGTH), nullable=False)
    accepted = db.Column(db.Boolean, default=False)
    images = db.relationship('AdImage', backref='ad', lazy=True)
    comments = db.relationship('Comment', backref='ad', lazy=True, cascade='all, delete-orphan')
    user_id = db.Column(db.String(100), nullable=False)  # Зв'язок з користувачем
    #user = db.relationship('User', backref='ads', lazy=True)  # Відворотній зв'язок
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Ad {self.title}>"

    @validates('description')
    def validate_description(self, key, value):
        if len(value) > MAX_DESCRIPTION_LENGTH:
            raise ValueError(f"{key.capitalize()} cannot exceed {MAX_DESCRIPTION_LENGTH} characters.")
        return value

    @validates('title')
    def validate_title(self, key, value):
        if len(value) > MAX_TITLE_LENGTH:
            raise ValueError(f"{key.capitalize()} cannot exceed {MAX_TITLE_LENGTH} characters.")
        return value

    @validates('location')
    def validate_location(self, key, value):
        if len(value) > MAX_LOCATION_LENGTH:
            raise ValueError(f"{key.capitalize()} cannot exceed {MAX_LOCATION_LENGTH} characters.")
        return value

    @validates('price')
    def validate_price(self, key, value):
        if value < MIN_PRICE or value > MAX_PRICE:
            raise ValueError(f"{key.capitalize()} must be between {MIN_PRICE} and {MAX_PRICE}.")
        return value

    def save(self):
        """Зберегти заявку."""
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        """Оновити заявку."""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        db.session.commit()

    def delete(self):
        """Видалити заявку."""
        db.session.delete(self)
        db.session.commit()

    def accept(self):
        """Позначити заявку як прийняту."""
        self.accepted = True
        db.session.commit()

    @staticmethod
    def find_by_id(ad_id):
        """Знайти заявку за ID."""
        return Ad.query.get(ad_id)


class AdImage(db.Model):
    """Модель для збереження зображень заявки."""
    __tablename__ = 'ad_images'

    id = db.Column(db.Integer, primary_key=True)
    ad_id = db.Column(db.Integer, db.ForeignKey('ads.id'), nullable=False)
    image_url = db.Column(db.String(MAX_URL_LENGTH), nullable=False)

    @validates('url')
    def validate_description(self, key, value):
        if len(value) > MAX_TITLE_LENGTH:
            raise ValueError(f"{key.capitalize()} cannot exceed {MAX_URL_LENGTH} characters.")
        return value

    def save(self):
        """Зберегти запис зображення в базу даних."""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Видалити фотки."""
        db.session.delete(self)
        db.session.commit()

    def update(self, data):
        """Оновити зображення."""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        db.session.commit()

    @staticmethod
    def find_by_id(id):
        """Знайти заявку за ID."""
        return AdImage.query.get(id)


class Comment(db.Model):
    """Модель для коментарів до оголошень."""
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    ad_id = db.Column(db.Integer, db.ForeignKey('ads.id'), nullable=False)
    user_id = db.Column(db.String(100), nullable=False)  # ID користувача, який залишив коментар
    content = db.Column(db.String(MAX_COMMENT_LENGTH), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @validates('content')
    def validate_content(self, key, value):
        if len(value) > MAX_COMMENT_LENGTH:
            raise ValueError(f"Comment cannot exceed {MAX_COMMENT_LENGTH} characters.")
        if len(value.strip()) == 0:
            raise ValueError("Comment cannot be empty.")
        return value

    def save(self):
        """Зберегти коментар."""
        db.session.add(self)
        db.session.commit()

    def update(self, content):
        """Оновити коментар."""
        self.content = content
        self.updated_at = datetime.utcnow()
        db.session.commit()

    def delete(self):
        """Видалити коментар."""
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def find_by_id(comment_id):
        """Знайти коментар за ID."""
        return Comment.query.get(comment_id)

    def __repr__(self):
        return f"<Comment {self.id} by {self.user_id}>"


class UserRating(db.Model):
    """Модель для рейтингу користувачів."""
    __tablename__ = 'user_ratings'

    id = db.Column(db.Integer, primary_key=True)
    rated_user_id = db.Column(db.String(100), nullable=False)  # ID користувача, якого оцінюють
    rater_user_id = db.Column(db.String(100), nullable=False)  # ID користувача, який оцінює
    ad_id = db.Column(db.Integer, db.ForeignKey('ads.id'), nullable=False)  # Оголошення, за яке ставиться оцінка
    rating = db.Column(db.Integer, nullable=False)  # Оцінка від 1 до 5
    comment = db.Column(db.String(MAX_COMMENT_LENGTH), nullable=True)  # Необов'язковий коментар до оцінки
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Унікальний індекс: один користувач може оцінити іншого тільки один раз за одне оголошення
    __table_args__ = (db.UniqueConstraint('rated_user_id', 'rater_user_id', 'ad_id', name='unique_rating'),)

    @validates('rating')
    def validate_rating(self, key, value):
        if value < 1 or value > 5:
            raise ValueError("Rating must be between 1 and 5.")
        return value

    @validates('comment')
    def validate_comment(self, key, value):
        if value and len(value) > MAX_COMMENT_LENGTH:
            raise ValueError(f"Rating comment cannot exceed {MAX_COMMENT_LENGTH} characters.")
        return value

    def save(self):
        """Зберегти рейтинг."""
        db.session.add(self)
        db.session.commit()

    def update(self, rating, comment=None):
        """Оновити рейтинг."""
        self.rating = rating
        if comment is not None:
            self.comment = comment
        self.updated_at = datetime.utcnow()
        db.session.commit()

    def delete(self):
        """Видалити рейтинг."""
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def find_by_id(rating_id):
        """Знайти рейтинг за ID."""
        return UserRating.query.get(rating_id)

    @staticmethod
    def get_user_average_rating(user_id):
        """Отримати середній рейтинг користувача."""
        result = db.session.query(db.func.avg(UserRating.rating)).filter_by(rated_user_id=user_id).scalar()
        return round(result, 2) if result else 0.0

    @staticmethod
    def get_user_ratings_count(user_id):
        """Отримати кількість оцінок користувача."""
        return UserRating.query.filter_by(rated_user_id=user_id).count()

    def __repr__(self):
        return f"<UserRating {self.rating}/5 for {self.rated_user_id}>"