import email
import logging
from app import db
from app.models.users_model import User
from flask import current_app
from app.models.users_model import User
from app import db
from sqlalchemy.exc import SQLAlchemyError



class UserRepository:
    @staticmethod
    def create_user(data):
        """
        Create a new user and save it to the database.
        :param data: Dictionary containing user details
        :return: Created user object or error message
        """
        try:
        # Create a User instance from the provided data
            user = User(
                name=data.get('name'),
                email=data.get('email'),
                role=data.get('role', 'member'),  # Default role is 'member'
                phone=data.get('phone'),
                profile_picture=data.get('profile_picture'),
                admin_id=data.get('admin_id'),
            )

        # Set password hash
            user.set_password(data['password'])

        # Add the user to the session and commit
            db.session.add(user)
            db.session.commit()

            return {"message": "User created successfully!", "user": user.serialize()}, 201

        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": "Database error", "details": str(e)}, 500

        except Exception as e:
            return {"error": "An unexpected error occurred", "details": str(e)}, 500

    
class UserRepository:
    
    @staticmethod
    def get_user_by_email(email):
        return User.query.filter_by(email=email).first()   
    
    @staticmethod
    def get_all_users():
        return User.query.all()

    @staticmethod
    def get_user_by_id(user_id):
        return User.query.get(user_id)

    @staticmethod
    def update_user(user_id, **data):
        user = User.query.get(user_id)
        if user:
            for key, value in data.items():
                setattr(user, key, value)
            db.session.commit()
            return user
        return None

    @staticmethod
    def delete_user(user_id):
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return user
        return None
