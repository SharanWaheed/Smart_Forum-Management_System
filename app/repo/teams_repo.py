from app.models.teams_model import Team, team_users
from app import db
from app.models.users_model import User

class TeamRepository:
    @staticmethod
    def create_team(name, description, admin_id):
        new_team = Team(name=name, description=description, admin_id=admin_id)
        db.session.add(new_team)
        db.session.commit()
        return new_team
    
    @staticmethod
    def get_all_teams():
        return Team.query.all()

    @staticmethod
    def get_team_by_id(team_id):
        return Team.query.get(team_id)

    @staticmethod
    def update_team(team_id, **kwargs):
        team = Team.query.get(team_id)
        if team:
            for key, value in kwargs.items():
                setattr(team, key, value)
            db.session.commit()
            return team
        return None

    @staticmethod
    def delete_team(team_id):
        team = Team.query.get(team_id)
        if team:
            db.session.delete(team)
            db.session.commit()
            return {"message": "Team deleted successfully."}
        return {"message": "Team not found."}

    @staticmethod
    def get_users_in_team(team_id):
        team = Team.query.get(team_id)
        if team:
            return team.users
        return None

    @staticmethod
    def save(team):
        db.session.commit()
