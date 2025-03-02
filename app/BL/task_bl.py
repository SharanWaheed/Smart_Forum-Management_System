from app import db
from app.repo.task_repo import TaskRepository
from app.models.association import project_tasks


class TaskBL:
    @staticmethod
    def create_task(data):
        """Process task creation logic."""
        title = data.get("title")
        description = data.get("description")
        due_date = data.get("due_date")
        projects = data.get("projects", [])  # Expecting project IDs as a list

        if not title or not due_date:
            return {"error": "Title and Due Date are required"}, 400

        # Create task and link it with projects
        new_task = TaskRepository.create_task(title, description, due_date, projects)
        return new_task

    @staticmethod
    def get_all_tasks():
        """Fetch all tasks."""
        return TaskRepository.get_all_tasks()

    @staticmethod
    def get_task_by_id(task_id):
        """Fetch a task by ID."""
        return TaskRepository.get_task_by_id(task_id)

    @staticmethod
    def update_task(task_id, **kwargs):  #  Accept dynamic fields
        task = TaskRepository.get_task_by_id(task_id)
        if not task:
            return None  # Task not found

        for key, value in kwargs.items():  # Dynamically update only provided fields
            setattr(task, key, value)

        try:
            db.session.commit()  # Commit changes
            return task
        except Exception as e:
            db.session.rollback()  #Rollback if error occurs
            raise  

    @staticmethod
    def delete_task(task_id):
        """Delete a task."""
        success = TaskRepository.delete_task(task_id)
        if not success:
            return {"error": "Task not found"}, 404
        return {"message": "Task deleted successfully"}


from app.repo.task_repo import TaskRepository

class TaskBL:
    @staticmethod
    def assign_task_to_project(task_id, project_id):
        """Assign a task to a project"""
        return TaskRepository.assign_task_to_project(task_id, project_id)
    
    @staticmethod
    def remove_task_from_project(task_id, project_id):
        """Remove a task from a specific project (removes from project_tasks table)"""
        return TaskRepository.remove_task_from_project(project_id, task_id)
