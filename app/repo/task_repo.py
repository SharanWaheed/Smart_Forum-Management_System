from sqlalchemy import delete
from app.models.task_model import Task
from app.models.association import project_tasks
from app import db

class TaskRepository:
    @staticmethod
    def create_task(title, description, due_date, projects=None):
        """Create a new task and associate it with projects."""
        new_task = Task(title=title, description=description, due_date=due_date)
        if projects:
            new_task.projects.extend(projects)

        db.session.add(new_task)
        db.session.commit()
        return new_task

    @staticmethod
    def get_all_tasks():
        """Retrieve all tasks."""
        return Task.query.all()

    @staticmethod
    def get_task_by_id(task_id):
        """Retrieve a single task by ID."""
        return Task.query.get(task_id)

    @staticmethod
    def update_task(task_id, **kwargs): 
        """Update an existing task."""
        task = Task.query.get(task_id)
        if not task:
            return None

        for key, value in kwargs.items():
            if value is not None:  # Prevent overwriting with None
                setattr(task, key, value)

        db.session.commit()
        return task

    @staticmethod
    def delete_task(task_id):
        """Delete a task by ID."""
        task = Task.query.get(task_id)
        if not task:
            return False

        db.session.delete(task)
        db.session.commit()
        return True

    @staticmethod
    def assign_task_to_project(task_id, project_id):
        """Insert task assignment into project_tasks table"""
        try:
            insert_statement = project_tasks.insert().values(project_id=project_id, task_id=task_id)
            db.session.execute(insert_statement)
            db.session.commit()
            return {"message": "Task assigned successfully"}
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 500


    @staticmethod
    def remove_task_from_project(project_id, task_id):
        """Remove a task from a project."""
        delete_stmt = delete(project_tasks).where(
            (project_tasks.c.project_id == project_id) & (project_tasks.c.task_id == task_id)
        )
        result = db.session.execute(delete_stmt)

        if result.rowcount == 0:
            return False

        db.session.commit()
        return True
