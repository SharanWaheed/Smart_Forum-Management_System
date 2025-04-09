from flask import Blueprint, jsonify, request
from webargs.flaskparser import use_args
from marshmallow import fields, ValidationError
from app.BL.task_bl import TaskBL
from app.schema.task_schema import TaskSchema, TaskUpdateSchema

task_bp = Blueprint("task_bp", __name__, url_prefix="/tasks")


@task_bp.route("/create", methods=["POST"])
@use_args(TaskSchema(), location="json")
def create_task(args):
    """API to create a task"""
    return TaskBL.create_task(args)


@task_bp.route("/", methods=["GET"])
def get_all_tasks():
    """API to retrieve all tasks"""
    return TaskBL.get_all_tasks()


@task_bp.route("/get-task", methods=["GET"])
def get_task():
    """API to get a specific task by ID"""
    data = request.get_json()
    task_id = data["task_id"]
    task = TaskBL.get_task_by_id(task_id)
    return jsonify({"task": TaskSchema().dump(task)})


@task_bp.route("/update", methods=["PUT"])
@use_args(TaskUpdateSchema(), location="json")  # Use TaskUpdateSchema
def update_task(args):
    """API to update a task"""
    task_id = args.pop("task_id")  # Extract task_id separately
    return TaskBL.update_task(task_id, args)  # Pass task_id separately


@task_bp.route("/delete", methods=["DELETE"])
@use_args({"task_id": fields.Int(required=True)}, location="json")
def delete_task(args):
    """API to delete a task"""
    return TaskBL.delete_task(args["task_id"])


@task_bp.route("/assign", methods=["POST"])
@use_args({"task_id": fields.Int(required=True), "project_id": fields.Int(required=True)}, location="json")
def assign_task_to_project(args):
    """API to assign a task to a project"""
    return TaskBL.assign_task_to_project(args["task_id"], args["project_id"])


@task_bp.route("/remove", methods=["DELETE"])
@use_args({"task_id": fields.Int(required=True), "project_id": fields.Int(required=True)}, location="json")
def remove_task(args):
    """API to remove a task from a project"""
    return TaskBL.remove_task_from_project(args["task_id"], args["project_id"])
