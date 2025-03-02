from datetime import date, datetime
from flask import Blueprint, jsonify
from webargs.flaskparser import use_args
from app import db
from app.BL.project_bl import ProjectBL
from app.models.project_model import Project
from app.schema import project_schema
from app.schema.project_schema import ProjectSchema, projects_schema
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required

project_bp = Blueprint('project_bp', __name__, url_prefix='/projects')

@project_bp.route('/create', methods=['POST'])
@use_args(project_schema, location="json")  # Ensures JSON body is validated
def create_project(args):
    try:
        # No need to parse start_date and end_date again; Marshmallow already handles it
        new_project = Project(
            name=args["name"],
            description=args.get("description"),
            start_date=args["start_date"],  # These are already date objects
            end_date=args["end_date"]
        )

        db.session.add(new_project)
        db.session.commit()

        return jsonify({
            "message": "Project created successfully",
            "project": project_schema.dump(new_project)
        }), 201

    except ValidationError as err:
        return jsonify({"error": err.messages}), 400  # Handle validation errors
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Handle unexpected errors


@project_bp.route('/all', methods=['GET'])
#@jwt_required()
def get_all_projects():
    """API endpoint to get all projects"""
    try:
        projects = ProjectBL.get_all_projects()
        return jsonify({"projects": projects_schema.dump(projects)}), 200
    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500

@project_bp.route('/update', methods=['PUT'])
@use_args(ProjectSchema(partial=True), location="json")  # Allow partial updates
def update_project(args):
    """API endpoint to update a project"""
    try:
        project_id = args.get("id")
        if not project_id:
            return jsonify({"error": "Project ID is required"}), 400
        
        # ✅ Remove ID from args before passing to update_project()
        args.pop("id", None)

        # ✅ Fix: Unpack `args` using `**` to pass as keyword arguments
        updated_project = ProjectBL.update_project(project_id, **args)  
        if not updated_project:
            return jsonify({"message": "Project not found"}), 404

        return jsonify({
            "message": "Project updated successfully",
            "project": ProjectSchema().dump(updated_project)
        }), 200

    except ValidationError as ve:
        return jsonify({"errors": ve.messages}), 422
    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500
    
    
    

@project_bp.route('/delete/<int:project_id>', methods=['DELETE'])
@jwt_required()
def delete_project(project_id):
    """API endpoint to delete a project"""
    try:
        deleted = ProjectBL.delete_project(project_id)
        if not deleted:
            return jsonify({"message": "Project not found"}), 404
        return jsonify({"message": "Project deleted successfully"}), 200
    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500
