from app.models.project_model import Project, db

class ProjectRepository:
    @staticmethod
    def create_project(name, start_date, end_date, description=None):
        try:
            project = Project(name=name, start_date=start_date, end_date=end_date, description=description)
            db.session.add(project)
            db.session.commit()
            return project
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_project_by_id(project_id):
        return Project.query.get(project_id)

    @staticmethod
    def get_all_projects():
        return Project.query.all()

    @staticmethod
    def update_project(project_id, name=None, start_date=None, end_date=None, description=None):
        project = Project.query.get(project_id)
        if not project:
            return None
        if name:
            project.name = name
        if start_date:
            project.start_date = start_date
        if end_date:
            project.end_date = end_date
        if description:
            project.description = description
        db.session.commit()
        return project

    @staticmethod
    def delete_project(project_id):
        project = Project.query.get(project_id)
        if project:
            db.session.delete(project)
            db.session.commit()
            return True
        return False
