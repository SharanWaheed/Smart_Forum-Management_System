# Import all models here so they're available for migrations
from app.models.admin_model import Admin
from app.models.users_model import User 
from app.models.teams_model import Team  
from .users_model import User
from .teams_model import Team, team_users  # Import Team and team_users from teams_model

__all__ = ['User', 'Team','Admin', 'team_users']  # Explicitly expose User, Team, and team_users
