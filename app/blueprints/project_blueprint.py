from marshmallow import fields  
from flask import Blueprint, jsonify
from webargs.flaskparser import use_args
from app.BL.project_bl import ProjectBL
from app.schema.project_schema import ProjectSchema, projects_schema

project_bp = Blueprint('project_bp', __name__, url_prefix='/projects')


@project_bp.route('/create', methods=['POST'])
@use_args(ProjectSchema(), location="json")
def create_project(args):
    project = ProjectBL.create_project(**args)
    return jsonify({"message": "Project created successfully", "project": ProjectSchema().dump(project)}), 201


@project_bp.route('/all', methods=['GET'])
def get_all_projects():
    projects = ProjectBL.get_all_projects()
    return jsonify({"projects": projects_schema.dump(projects)}), 200



@project_bp.route('/update', methods=['PUT'])
@use_args(ProjectSchema(), location="json")
def update_project(args):
    project_id = args.pop("id", None)
    updated_project = ProjectBL.update_project(project_id, **args)
    return jsonify({"message": "Project updated successfully", "project": ProjectSchema().dump(updated_project)}), 200


@project_bp.route('/delete', methods=['DELETE'])
@use_args({"id": fields.Int(required=True)}, location="json")
def delete_project(args):
    project_id = args["id"]
    ProjectBL.delete_project(project_id)
    return jsonify({"message": "Project deleted successfully"}), 200


