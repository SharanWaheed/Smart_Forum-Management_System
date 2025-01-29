from app import db
from datetime import datetime
from sqlalchemy.orm import relationship

# Many-to-Many relationship table
team_users = db.Table(
    'team_users',
    db.Column('team_id', db.Integer, db.ForeignKey('teams.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
) 
                                   
class Team(db.Model):
    __tablename__ = 'teams'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    admin_id = db.Column(db.Integer, db.ForeignKey('admins.id'), nullable=False)

    # Relationships
    admin = db.relationship('Admin', backref='teams')  # One-to-Many with Admin
    users = db.relationship('User', secondary=team_users, back_populates='teams')  # Many-to-Many with User
