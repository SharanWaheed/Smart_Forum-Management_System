from app.models.admin_model import Admin
from app import db
from sqlalchemy.orm import joinedload

class AdminRepository:
    @staticmethod
    def create_admin(name, email, password):
        new_admin = Admin(name=name, email=email, password=password)
        db.session.add(new_admin)
        db.session.commit()
        return new_admin

    
     
    def get_all_admins_with_users(page=1, per_page=5):
        """
        Fetch paginated admins with related users eagerly loaded.
        Returns a Pagination object, not just the items.
        """
        return Admin.query.options(joinedload(Admin.users)) \
            .paginate(page=page, per_page=per_page, error_out=False)

    
    @staticmethod
    def get_admin_by_id(admin_id):
        return Admin.query.get(admin_id)

    @staticmethod
    def get_admin_by_email(email):
        return Admin.query.filter_by(email=email).first()

    @staticmethod
    def update_admin(admin_id, **kwargs):
        admin = Admin.query.get(admin_id)
        if not admin:
            return None

        # Update fields dynamically using kwargs
        for key, value in kwargs.items():
            setattr(admin, key, value)

        db.session.commit()
        return admin

    @staticmethod
    def delete_admin(admin_id):
        admin = Admin.query.get(admin_id)
        if admin:
            db.session.delete(admin)
            db.session.commit()
        return admin
