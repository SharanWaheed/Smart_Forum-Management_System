from datetime import datetime
from app import db  # Use the db instance from app.__init__.py
from app.models.association import project_tasks
from sqlalchemy.orm import relationship 

# Association Table (Define this before Project & Task)


class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Use a string reference instead of direct Task reference
    tasks = db.relationship('Task', secondary=project_tasks, back_populates='projects')
    allocations = relationship("ResourceAllocation", back_populates="project", cascade="all, delete-orphan")
    def __init__(self, name, start_date, end_date, description=None):
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.description = description
