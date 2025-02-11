from app import db
from app.models.association import users_roles  # Import from the new file

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    users = db.relationship('User', secondary=users_roles, back_populates='roles')