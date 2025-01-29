from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

 
class User(db.Model):
    __tablename__ = 'users'

    # Define the fields for the User model
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), default='member')  # Default role as member
    is_active = db.Column(db.Boolean, default=True)  # Active status
    phone = db.Column(db.String(15), nullable=True)  # Optional field
    profile_picture = db.Column(db.String(255), nullable=True)  # Optional field
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Foreign Key with Admin
    admin_id = db.Column(db.Integer, db.ForeignKey('admins.id', ondelete='SET NULL'))  
    admin = relationship("Admin", back_populates="users", foreign_keys=[admin_id])

    # Many-to-Many Relationship with Team
    teams = db.relationship('Team', secondary='team_users', back_populates='users')
    
    def serialize(self):
        """
        Serialize the User object to a dictionary.
        """
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "role": self.role,
            "is_active": self.is_active,
            "phone": self.phone,
            "profile_picture": self.profile_picture,
            "admin_id": self.admin_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password)

    # Serialize method to convert User object to JSON-compatible dict
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'role': self.role,
            'is_active': self.is_active,
            'phone': self.phone,
            'profile_picture': self.profile_picture,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'admin_id': self.admin_id
        }
