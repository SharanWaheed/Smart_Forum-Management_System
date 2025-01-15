from app.models.teams_model import Team
from app.repo.teams_repo import TeamRepository
from app.repo.users_repo import UserRepository

class TeamBL:
    @staticmethod
    def create_team(name, description, admin_id):
        try:
            new_team = TeamRepository.create_team(name=name, description=description, admin_id=admin_id)
            return new_team, 201
        except Exception as e:
            return {"message": f"An error occurred: {str(e)}"}, 500

    @staticmethod
    def get_all_teams():
        teams = TeamRepository.get_all_teams()
        return teams

    @staticmethod
    def get_team_by_id(team_id):
        team = TeamRepository.get_team_by_id(team_id)
        if not team:
            return {"message": "Team not found."}, 404
        return team, 200

    @staticmethod
    def update_team(team_id, **kwargs):
        try:
            updated_team = TeamRepository.update_team(team_id, **kwargs)
            if not updated_team:
                return {"message": "Team not found."}, 404
            return updated_team, 200
        except Exception as e:
            return {"message": f"An error occurred: {str(e)}"}, 500

    @staticmethod
    def delete_team(team_id):
        try:
            deleted_team = TeamRepository.delete_team(team_id)
            if not deleted_team:
                return {"message": "Team not found."}, 404
            return {"message": "Team deleted successfully."}, 200
        except Exception as e:
            return {"message": f"An error occurred: {str(e)}"}, 500

    @staticmethod
    def add_user_to_team(team_id, user_id):
        try:
            team = TeamRepository.get_team_by_id(team_id)
            user = UserRepository.get_user_by_id(user_id)
            if not team or not user:
                return {"message": "Team or User not found."}, 404
            
            if user in team.users:
                return {"message": "User is already a member of this team."}, 400
            
            team.users.append(user)  # Add the user to the team
            TeamRepository.save(team)  # Save changes
            return {"message": "User added to the team successfully."}, 200
        except Exception as e:
            return {"message": f"An error occurred: {str(e)}"}, 500

    @staticmethod
    def remove_user_from_team(team_id, user_id):
        try:
            team = TeamRepository.get_team_by_id(team_id)
            user = UserRepository.get_user_by_id(user_id)
            if not team or not user:
                return {"message": "Team or User not found."}, 404
            
            if user not in team.users:
                return {"message": "User is not a member of this team."}, 400
            
            team.users.remove(user)  # Remove the user from the team
            TeamRepository.save(team)  # Save changes
            return {"message": "User removed from the team successfully."}, 200
        except Exception as e:
            return {"message": f"An error occurred: {str(e)}"}, 500

    @staticmethod
    def get_users_in_team(team_id):
        try:
            team = Team.query.get(team_id)
            if not team:
                return {"message": "Team not found"}, 404
            
            # Convert users to a serializable format
            users_list = [
                {"id": user.id, "name": user.name, "email": user.email}
                for user in team.users
            ]

            return {
                "team_id": team.id,
                "team_name": team.name,
                "users": users_list
            }, 200
        except Exception as e:
            return {"message": f"An error occurred: {str(e)}"}, 500 
