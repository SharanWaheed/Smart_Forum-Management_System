from werkzeug.security import generate_password_hash
from app import db
from app.repo.admin_repo import AdminRepository
from app.models.admin_model import Admin
from werkzeug.security import generate_password_hash

from app.schema.admin_schema import AdminSchema

class AdminBL:
    @staticmethod
    def create_admin(name, email, password):
        try:
            # Hash the password before saving it
            hashed_password = generate_password_hash(password)

            # Call the repository method to create the admin in the database
            new_admin = AdminRepository.create_admin(name, email, hashed_password)  # Pass the hashed password
            
            # Serialize the new admin using the AdminSchema
            admin_schema = AdminSchema()
            serialized_admin = admin_schema.dump(new_admin)
            
            return serialized_admin, 201
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
        admin = Admin.query.get(int(admin_id))
        if not admin:
            return {"error": "Admin not found"}, 404  # Return a tuple

        for key, value in kwargs.items():
            setattr(admin, key, value)  # Dynamically update fields

        db.session.commit()
        return admin, 200

    @staticmethod
    def delete_admin(admin_id):
        try:
            deleted_admin = AdminRepository.delete_admin(admin_id)
            if not deleted_admin:
                return {"message": "Admin not found."}, 404
            return {"message": "Admin deleted successfully."}, 200
        except Exception as e:
            return {"message": f"An error occurred: {str(e)}"}, 500
