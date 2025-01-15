from werkzeug.security import generate_password_hash
from app.repo.admin_repo import AdminRepository
from app.models.admin_model import Admin

class AdminBL:
    @staticmethod
    def create_admin(name, email, password):
        # Check if the email already exists
        if AdminRepository.get_admin_by_email(email):
            return {"message": "Email already exists."}, 400
        
        try:
            hashed_password = generate_password_hash(password)
            new_admin = AdminRepository.create_admin(name=name, email=email, password=hashed_password)
            return new_admin, 201
        except Exception as e:
            return {"message": f"An error occurred: {str(e)}"}, 500

    @staticmethod
    def get_all_admins(): 
        return AdminRepository.get_all_admins()

    @staticmethod
    def get_admin_by_id(admin_id):
        admin = AdminRepository.get_admin_by_id(admin_id)
        if not admin:
            return {"message": "Admin not found."}, 404
        return admin, 200

    @staticmethod
    def update_admin(admin_id, **kwargs):
        try:
            hashed_password = (
                generate_password_hash(kwargs.get("password")) if kwargs.get("password") else None
            )
            kwargs["password"] = hashed_password
            updated_admin = AdminRepository.update_admin(admin_id, **kwargs)
            if not updated_admin:
                return {"message": "Admin not found."}, 404
            return updated_admin, 200
        except Exception as e:
            return {"message": f"An error occurred: {str(e)}"}, 500

    @staticmethod
    def delete_admin(admin_id):
        try:
            deleted_admin = AdminRepository.delete_admin(admin_id)
            if not deleted_admin:
                return {"message": "Admin not found."}, 404
            return {"message": "Admin deleted successfully."}, 200
        except Exception as e:
            return {"message": f"An error occurred: {str(e)}"}, 500
