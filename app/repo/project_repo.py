from app.models.project_model import Project, db

class ProjectRepository:
    @staticmethod
    def create_project(name, start_date, end_date, description=None):
        """Creates a new project in the database."""
        try:
            project = Project(name=name, start_date=start_date, end_date=end_date, description=description)
            db.session.add(project)
            db.session.commit()
            return project
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Database error while creating project: {str(e)}")

    @staticmethod
    def get_project_by_id(project_id):
        """Fetches a project by its ID."""
        return Project.query.get(project_id)

    @staticmethod
    def get_all_projects():
        """Retrieves all projects from the database."""
        return Project.query.all()

    @staticmethod
    def update_project(project_id, name=None, start_date=None, end_date=None, description=None):
        """Updates an existing project."""
        try:
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
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Database error while updating project: {str(e)}")

    @staticmethod
    def delete_project(project_id):
        """Deletes a project from the database."""
        try:
            project = Project.query.get(project_id)
            if not project:
                return False
            
            db.session.delete(project)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Database error while deleting project: {str(e)}")
