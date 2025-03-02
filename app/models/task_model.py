from datetime import datetime
from app import db  # Use the db instance from app.__init__.py
from app.models.association import project_tasks
from sqlalchemy.orm import relationship

class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    due_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Use a string reference to avoid circular imports
    projects = db.relationship('Project', secondary=project_tasks, back_populates='tasks')
    allocations = db.relationship("ResourceAllocation", back_populates="task", cascade="all, delete-orphan")
