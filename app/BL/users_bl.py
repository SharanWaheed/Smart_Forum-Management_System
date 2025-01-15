from werkzeug.security import generate_password_hash
from app import db
from app.models.users_model import User
from app.repo.users_repo import UserRepository

class UserBL:
    @staticmethod
    def create_user(data):
        try:
            # Hash the password before saving
            if "password" in data:
                data["password"] = generate_password_hash(data["password"])
            
            # Create the new user
            user = User(
                name=data['name'],
                email=data['email'],
                password=data['password'],
                role=data['role'],
                is_active=data['is_active'],
                phone=data.get('phone'),
                profile_picture=data.get('profile_picture'),
                admin_id=data['admin_id']
            )

            # Add the user to the session
            db.session.add(user)
            db.session.commit()

            # Return the serialized user
            return user.serialize(), 201
        except Exception as e:
            return {"message": f"An error occurred: {str(e)}"}, 500

    @staticmethod
    def get_all_users():
        try:
            users = UserRepository.get_all_users()
            return [user.serialize() for user in users], 200
        except Exception as e:
            return {"message": f"An error occurred: {str(e)}"}, 500

    @staticmethod
    def get_user_by_id(user_id):
        user = UserRepository.get_user_by_id(user_id)
        if not user:
            return {"message": "User not found."}, 404
        return user.serialize(), 200

    @staticmethod
    def update_user(user_id, data):
        try:
            if "password" in data:
                data["password"] = generate_password_hash(data["password"])
            
            updated_user = UserRepository.update_user(user_id, **data)
            if not updated_user:
                return {"message": "User not found."}, 404
            return {"message": "User updated successfully!", "user": updated_user.serialize()}, 200
        except Exception as e:
            return {"message": f"An error occurred: {str(e)}"}, 500

    @staticmethod
    def delete_user(user_id):
        try:
            deleted_user = UserRepository.delete_user(user_id)
            if not deleted_user:
                return {"message": "User not found."}, 404
            return {"message": "User deleted successfully!"}, 200
        except Exception as e:
            return {"message": f"An error occurred: {str(e)}"}, 500
