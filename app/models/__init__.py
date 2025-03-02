# Import db from association.py to ensure a single source of truth
from app.models.association import  project_tasks   # Association table for Task & Project
from app import db 
from app.models.allocation import ResourceAllocation
# Import all models here so they're available for migrations
from .admin_model import Admin
from .users_model import User
from .teams_model import Team, team_users  # Import Team and team_users from teams_model
from .project_model import Project
from .task_model import Task  # Import Task model
from .allocation import ResourceAllocation



# Explicitly expose all models
__all__ = ['db', 'User', 'Project', 'Task', 'Team', 'Admin', 'team_users', 'project_tasks'
           , 'ResourceAllocation'
           ]
