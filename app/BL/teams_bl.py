from app.models.teams_model import Team
from app.repo.teams_repo import TeamRepository
from app.repo.users_repo import UserRepository
from app.db import db

class TeamBL:
    
    @staticmethod
    def serialize_team(team):
        """Serialize a single team object."""
        return {
            "id": team.id,
            "name": team.name,
            "description": team.description,
            "admin_id": team.admin_id
        }
    
    @staticmethod
    def serialize_teams(teams):
        """Serialize a list of team objects."""
        return [TeamBL.serialize_team(team) for team in teams]

    @staticmethod
    def create_team(name, description, admin_id):
        """Create a new team."""
        try:
            new_team = TeamRepository.create_team(name=name, description=description, admin_id=admin_id)
            return TeamBL.serialize_team(new_team), 201
        except Exception as e:
            return {"message": f"An error occurred: {str(e)}"}, 500

    @staticmethod
    def get_all_teams():
        """Get all teams."""
        try:
            teams = TeamRepository.get_all_teams()
            return TeamBL.serialize_teams(teams)
        except Exception as e:
            return {"message": f"An error occurred: {str(e)}"}, 500

    @staticmethod
    def get_team_by_id(team_id):
        """Get a team by its ID."""
        team = TeamRepository.get_team_by_id(team_id)
        if not team:
            return {"message": "Team not found."}, 404
        return TeamBL.serialize_team(team), 200

    @staticmethod
    def update_team(team_id, **kwargs):
        """Update a team."""
        try:
            updated_team = TeamRepository.update_team(team_id, **kwargs)
            if not updated_team:
                return {"message": "Team not found."}, 404
            return TeamBL.serialize_team(updated_team), 200
        except Exception as e:
            return {"message": f"An error occurred: {str(e)}"}, 500

    @staticmethod
    def delete_team(team_id):
        """Delete a team."""
        try:
            deleted_team = TeamRepository.delete_team(team_id)
            if "not found" in deleted_team["message"]:
                return deleted_team, 404
            return deleted_team, 200
        except Exception as e:
            return {"message": f"An error occurred: {str(e)}"}, 500

    @staticmethod
    def add_user_to_team(team_id, user_id):
        """Add a user to a team."""
        try:
            team = TeamRepository.get_team_by_id(team_id)
            user = UserRepository.get_user_by_id(user_id)
            if not team or not user:
                return {"message": "Team or User not found."}, 404
            
            if user in team.users:
                return {"message": "User is already a member of this team."}, 400
            
            team.users.append(user)
            TeamRepository.save(team)
            return {"message": "User added to the team successfully."}, 200
        except Exception as e:
            return {"message": f"An error occurred: {str(e)}"}, 500

    @staticmethod
    def remove_user_from_team(team_id, user_id):
        """Remove a user from a team."""
        try:
            team = TeamRepository.get_team_by_id(team_id)
            user = UserRepository.get_user_by_id(user_id)
            if not team or not user:
                return {"message": "Team or User not found."}, 404
            
            if user not in team.users:
                return {"message": "User is not a member of this team."}, 400
            
            team.users.remove(user)
            TeamRepository.save(team)
            return {"message": "User removed from the team successfully."}, 200
        except Exception as e:
            return {"message": f"An error occurred: {str(e)}"}, 500

    @staticmethod
    def get_users_in_team(team_id):
        """Get all users in a team."""
        try:
            team = TeamRepository.get_team_by_id(team_id)
            if not team:
                return {"message": "Team not found."}, 404
            users_list = [{"id": user.id, "name": user.name, "email": user.email} for user in team.users]
            return {"team_id": team.id, "team_name": team.name, "users": users_list}, 200
        except Exception as e:
            return {"message": f"An error occurred: {str(e)}"}, 500
