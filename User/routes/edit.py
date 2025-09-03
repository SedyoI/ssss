'''from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from email_validator import validate_email, EmailNotValidError
#from User.models import User
from app import db
import re


edit_bp = Blueprint('edit', __name__)

@edit_bp.route('/profile/<int:user_id>/edit', methods=['PATCH'])
@jwt_required()
def edit_profile(user_id):

    current_user_id = get_jwt_identity()

    jwt_claims = get_jwt()
    user_role = jwt_claims.get("role")

    if not user_role:
        return jsonify({"error": "Role is missing in the token"}), 403

    if user_role == "admin":
        pass
    elif user_role == "user" and int(user_id) == int(current_user_id):
        pass
    else:
        return jsonify({"error": "Access denied"}), 403

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    allowed_fields = ["first_name", "last_name", "email", "phone"]

    errors = {}

    if "first_name" in data:
        if not isinstance(data["first_name"], str) or not re.match(r"^[a-zA-Z' -]+$", data["first_name"]):
            errors["first_name"] = "First name must contain only letters, spaces, hyphens, or apostrophes."

    if "last_name" in data:
        if not isinstance(data["last_name"], str) or not re.match(r"^[a-zA-Z' -]+$", data["last_name"]):
            errors["last_name"] = "Last name must contain only letters, spaces, hyphens, or apostrophes."

    if "email" in data:
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, data["email"]):
            errors["email"] = "Invalid email format."

    try:

        validated_email = validate_email(data["email"])
        data["email"] = validated_email.email  
    except EmailNotValidError as e:
        errors["email"] = str(e)

    if len(data["email"]) > 120:
        errors["email"] = "Email must not exceed 120 characters."


    if "phone" in data:
        phone_regex = r'^\+?\d{10,15}$'
    if not re.match(phone_regex, data["phone"]):
        errors["phone"] = "Phone number must be 10-15 digits, optionally starting with '+'."
    if errors:
        return jsonify({"error": "Validation errors", "details": errors}), 400

    for field in allowed_fields:
        if field in data:
            setattr(user, field, data[field])

    try:
        db.session.commit()
        return jsonify({"message": "Profile updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to update profile", "details": str(e)}), 500
'''