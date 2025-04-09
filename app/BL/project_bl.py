from datetime import datetime
from app.repo.project_repo import ProjectRepository

class ProjectBL:
    @staticmethod
    def create_project(name, start_date, end_date, description=None):
        """Handles project creation with error handling."""
        if not name:
            raise ValueError("Project name is required.")
        if not start_date:
            raise ValueError("Start date is required.")
        if not end_date:
            raise ValueError("End date is required.")
        if start_date > end_date:
            raise ValueError("Start date cannot be later than end date.")
        
        return ProjectRepository.create_project(name, start_date, end_date, description)
    
    @staticmethod
    def get_all_projects():
        """Retrieves all projects."""
        projects = ProjectRepository.get_all_projects()
        if not projects:
            raise ValueError("No projects found.")
        return projects
    
    @staticmethod
    def get_project_by_id(project_id):
        """Retrieves a specific project by ID with error handling."""
        if not project_id:
            raise ValueError("Project ID is required.")
        
        project = ProjectRepository.get_project_by_id(project_id)
        if not project:
            raise ValueError("Project not found.")
        return project
    
    @staticmethod
    def update_project(project_id, name=None, start_date=None, end_date=None, description=None):
        """Updates an existing project with error handling."""
        
         

        project = ProjectRepository.get_project_by_id(project_id)
        if not project:
            raise ValueError("Project not found.")
        
        if start_date and end_date and start_date > end_date:
            raise ValueError("Start date cannot be later than end date.")
        
        # do this in allocation file
        updated_project = ProjectRepository.update_project(project_id, name, start_date, end_date, description)
        return updated_project
    
    @staticmethod
    def delete_project(project_id):
        """Deletes a project by ID with error handling."""
        if not project_id:
            raise ValueError("Project ID is required.")
        
        deleted = ProjectRepository.delete_project(project_id)
        if not deleted:
            raise ValueError("Project not found.")
        return deleted
