from app import db
from sqlalchemy.orm import validates

MAX_PRICE = 1000000.0  # максимальна ціна
MIN_PRICE = 0.0  # мінімальна ціна
MAX_DESCRIPTION_LENGTH = 1000  # максимальна кількість символів для опису
MAX_TITLE_LENGTH = 100
MAX_LOCATION_LENGTH = 100
MAX_URL_LENGTH = 255


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
    user_id = db.Column(db.String(100), nullable=False)  # Зв'язок з користувачем
    #user = db.relationship('User', backref='ads', lazy=True)  # Відворотній зв'язок
    
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

