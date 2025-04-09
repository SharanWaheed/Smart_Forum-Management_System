from flask import jsonify
from app.repo.task_repo import TaskRepository
from app.schema.task_schema import TaskSchema

class TaskBL:
    @staticmethod
    def create_task(data):
        """Business logic for creating a task"""
        try:
            new_task = TaskRepository.create_task(
                title=data.get("title"),
                description=data.get("description"),
                due_date=data.get("due_date"),
                projects=data.get("projects", [])
            )
            return jsonify({"message": "Task created successfully", "task": new_task.to_dict()}), 201
        except Exception as e:
            return jsonify({"message": f"An error occurred: {str(e)}"}), 500

    @staticmethod
    def get_all_tasks():
        """Business logic for fetching all tasks"""
        try:
            tasks = TaskRepository.get_all_tasks()
            return jsonify({"tasks": [task.to_dict() for task in tasks]}), 200
        except Exception as e:
            return jsonify({"message": f"An error occurred: {str(e)}"}), 500

    @staticmethod
    def get_task_by_id(task_id):
        """Business logic for fetching a task by ID"""
        task = TaskRepository.get_task_by_id(task_id)
        if not task:
            return jsonify({"message": "Task not found"}), 404
        return jsonify({"task": task.to_dict()}), 200

    @staticmethod
    def update_task(task_id, data):
        """Business logic for updating a task"""
        try:
            if not task_id:
                return jsonify({"error": "Task ID is required"}), 400

            updated_task = TaskRepository.update_task(task_id, **data)
            if not updated_task:
                return jsonify({"message": "Task not found"}), 404

            return jsonify({"message": "Task updated successfully", "task": TaskSchema().dump(updated_task)}), 200
        except Exception as e:
            return jsonify({"message": f"An error occurred: {str(e)}"}), 500

    @staticmethod
    def delete_task(task_id):
        """Business logic for deleting a task"""
        success = TaskRepository.delete_task(task_id)
        if not success:
            return jsonify({"message": "Task not found"}), 404
        return jsonify({"message": "Task deleted successfully"}), 200

    @staticmethod
    def assign_task_to_project(task_id, project_id):
        """Business logic for assigning a task to a project"""
        return TaskRepository.assign_task_to_project(task_id, project_id)

    @staticmethod
    def remove_task_from_project(task_id, project_id):
        """Business logic for removing a task from a project"""
        success = TaskRepository.remove_task_from_project(project_id, task_id)
        if not success:
            return jsonify({"message": "Task not found in this project"}), 404
        return jsonify({"message": "Task removed from project successfully"}), 200
