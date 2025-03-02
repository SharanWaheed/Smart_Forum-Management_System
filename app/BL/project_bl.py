from datetime import datetime
from app.repo.project_repo import ProjectRepository

class ProjectBL:
    @staticmethod
    def create_project(name, start_date, end_date, description):
        """Creates a new project."""
        return ProjectRepository.create_project(name, start_date, end_date, description)

    @staticmethod
    def get_all_projects():
        """Retrieves all projects."""
        return ProjectRepository.get_all_projects()
     
    @staticmethod
    def get_project_by_id(project_id):
        """Retrieves a specific project by ID."""
        return ProjectRepository.get_project_by_id(project_id)

    @staticmethod
    def update_project(project_id, name=None, start_date=None, end_date=None, description=None):
        """Updates an existing project."""
        return ProjectRepository.update_project(project_id, name, start_date, end_date, description)

    @staticmethod
    def delete_project(project_id):
        """Deletes a project by ID."""
        return ProjectRepository.delete_project(project_id)
