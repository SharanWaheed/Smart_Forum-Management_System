import logging
from werkzeug.security import generate_password_hash
from app import db
from werkzeug.security import check_password_hash

from app.models.teams_model import Team
from app.models.users_model import User
from app.repo.users_repo import UserRepository
from werkzeug.security import check_password_hash

from app.models.teams_model import Team, team_users  # Import Team and team_users
from app.models.users_model import User  # Import User separately


from app import db

class UserBL:

 
    
    @staticmethod
    def authenticate_user(email, password):
        """
        Authenticate a user based on email and password.
        """
        user = UserRepository.get_user_by_email(email)  # Fetch user by email
        
        if user:  # Check if the user exists
            if check_password_hash(user.password, password):  # Verify the password
                return user  # Return the user if authentication is successful
            else:
                return None  # Password does not match
        else:
            return None

    @staticmethod
    def get_user_teams(user_id):
        """
        Fetch all teams associated with a user.
        """
        try:
            # Query to get teams linked to the user through the team_users table
            teams = db.session.query(Team).join(team_users).filter(team_users.c.user_id == user_id).all()
            return teams
        except Exception as e:
            logging.error(f"Error fetching teams for user {user_id}: {str(e)}")
            return None
    
    
 
    @staticmethod
    def create_user(data, admin_id):
        """
        Create a new user in the system.
        """
        try:
            print(f"Data passed to BL: {data}")  # Debug: Log incoming data to BL
            print(f"Admin ID from token: {admin_id}")  # Debug: Log admin ID from the token
            
            # Create a new User object
            user = User(
                name=data['name'],
                email=data['email'],
                password=generate_password_hash(data['password']),
                role=data.get('role', 'member'),  # Default role is 'member'
                is_active=data.get('is_active', True),  # Default is_active to True
                phone=data.get('phone'),
                profile_picture=data.get('profile_picture'),
                admin_id=admin_id  # Use admin_id from the token
            )
            
            # Add and commit the new user to the database
            db.session.add(user)
            db.session.commit()
            print("User created successfully!")  # Debug: Log success
            
            # Return success response
            return {"message": "User created successfully!", "user": user.serialize()}, 201
        except Exception as e:
            db.session.rollback()
            print(f"Error creating user: {str(e)}")  # Debug: Log exceptions
            return {"message": f"An error occurred: {str(e)}"}, 500

    @staticmethod
    def get_all_users():
        """
        Fetch all users in the system.
        """
        try:
            users = UserRepository.get_all_users()
            return [user.serialize() for user in users], 200
        except Exception as e:
            logging.error(f"Error fetching all users: {str(e)}")
            return {"message": f"An error occurred: {str(e)}"}, 500

    @staticmethod
    def get_user_by_id(user_id):
        """
        Fetch a specific user by ID.
        """
        user = UserRepository.get_user_by_id(user_id)
        if not user:
            return {"message": "User not found."}, 404
        return user.serialize(), 200

    @staticmethod
    def update_user(user_id, data):
        try:
            logging.debug(f"Received data for update: {data}")  # Debugging

            if "password" in data:
                data["password"] = generate_password_hash(data["password"])

            logging.debug(f"Data after password hashing: {data}")  # Debugging

            updated_user = UserRepository.update_user(user_id, **data)
            if not updated_user:
                return {"message": "User not found."}, 404
            
            return {"message": "User updated successfully!", "user": updated_user.serialize()}, 200

        except Exception as e:
            logging.error(f"Error updating user {user_id}: {str(e)}")
            return {"message": f"An error occurred: {str(e)}"}, 500

    @staticmethod
    def delete_user(user_id):
        """
        Delete a user by ID.
        """
        try:
            deleted_user = UserRepository.delete_user(user_id)
            if not deleted_user:
                return {"message": "User not found."}, 404
            return {"message": "User deleted successfully!"}, 200
        except Exception as e:
            logging.error(f"Error deleting user {user_id}: {str(e)}")
            return {"message": f"An error occurred: {str(e)}"}, 500