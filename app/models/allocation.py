from sqlalchemy import Column, Integer, ForeignKey, String, TIMESTAMP, func
from sqlalchemy.orm import relationship
from app import db # Import db from app, no need to redefine it

 

class ResourceAllocation(db.Model):
    __tablename__ = 'resource_allocations'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=True)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    role = db.Column(db.String(100), nullable=False)  # Fetched dynamically, not a FK
    assigned_at = db.Column(db.TIMESTAMP, server_default=func.now())
    status = db.Column(db.String(100), default='Active')  # Example: Active, Completed, Removed
    
    # Relationships
    project = db.relationship('Project', back_populates='allocations')
    task = db.relationship("Task", back_populates="allocations")  # FIXED
    user = db.relationship('User', back_populates='allocations')
    def __repr__(self):
        return f"<ResourceAllocation(user_id={self.user_id}, project_id={self.project_id}, task_id={self.task_id}, role={self.role}, status={self.status})>"
