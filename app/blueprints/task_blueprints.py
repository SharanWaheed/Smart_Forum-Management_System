
from flask import Blueprint, jsonify, request
from webargs.flaskparser import use_args
from app.BL.task_bl import TaskBL
from app.schema.task_schema import TaskSchema
from marshmallow import ValidationError, fields

task_bp = Blueprint("task_bp", __name__, url_prefix="/tasks")

@task_bp.route("/create", methods=["POST"])
@use_args(TaskSchema(), location="json")
def create_task(args):
    """API to create a task"""
    try:
        new_task = TaskBL.create_task(args)
        return jsonify({"message": "Task created successfully", "task": TaskSchema().dump(new_task)}), 201
    except ValidationError as ve:
        return jsonify({"errors": ve.messages}), 422
    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500

@task_bp.route("/", methods=["GET"])
def get_all_tasks():
    """API to retrieve all tasks"""
    try:
        tasks = TaskBL.get_all_tasks()
        return jsonify({"tasks": TaskSchema(many=True).dump(tasks)}), 200
    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500

@task_bp.route("/<int:task_id>", methods=["GET"])
def get_task(task_id):
    """API to get a specific task by ID"""
    try:
        task = TaskBL.get_task_by_id(task_id)
        if not task:
            return jsonify({"message": "Task not found"}), 404
        return jsonify({"task": TaskSchema().dump(task)}), 200
    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500

@task_bp.route("/update", methods=["PUT"])
@use_args(TaskSchema(partial=True), location="json")  #Allow partial updates
def update_task(args):
    """API to update a task (ID included in payload)"""
    try:
        task_id = args.pop("id", None)  #Extract ID separately
        if not task_id:
            return jsonify({"error": "Task ID is required"}), 400

        updated_task = TaskBL.update_task(task_id, **args)  #Now passes only valid fields
        if not updated_task:
            return jsonify({"message": "Task not found"}), 404

        return jsonify({"message": "Task updated successfully", "task": TaskSchema().dump(updated_task)}), 200
    except ValidationError as ve:
        return jsonify({"errors": ve.messages}), 422
    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500





@task_bp.route("/delete/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    """API to delete a task"""
    try:
        response = TaskBL.delete_task(task_id)
        if isinstance(response, tuple):  # Handles error responses
            return jsonify(response[0]), response[1]
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500





@task_bp.route("/assign", methods=["POST"])
@use_args({"task_id": fields.Int(required=True), "project_id": fields.Int(required=True)}, location="json")
def assign_task_to_project(args):
    """API to assign a task to a project"""
    try:
        task_id = args["task_id"]
        project_id = args["project_id"]

        assigned_task = TaskBL.assign_task_to_project(task_id, project_id)
        if isinstance(assigned_task, tuple):  # Handle errors
            return jsonify(assigned_task[0]), assigned_task[1]

        return jsonify({"message": "Task assigned to project successfully"}), 200
    except ValidationError as ve:
        return jsonify({"errors": ve.messages}), 422
    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500
    
    
@task_bp.route("/remove", methods=["DELETE"])
@use_args({"task_id": fields.Int(required=True), "project_id": fields.Int(required=True)}, location="json")
def remove_task(args):
    """API to remove a task from a project (removes from project_tasks table but doesn't delete task)"""
    try:
        print("Request received:", args)  # Log the received request
        task_id = args["task_id"]
        project_id = args["project_id"]

        success = TaskBL.remove_task_from_project(task_id, project_id)
        
        if not success:
            return jsonify({"message": "Task not found in this project"}), 404

        return jsonify({"message": "Task removed from project successfully"}), 200
    except ValidationError as ve:
        print("Validation Error:", ve.messages)
        return jsonify({"errors": ve.messages}), 422
    except Exception as e:
        print("Exception:", str(e))  # Log the error
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500