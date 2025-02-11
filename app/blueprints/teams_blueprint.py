from dataclasses import fields
from flask import Blueprint, request, jsonify
from app.BL.teams_bl import TeamBL
from webargs.flaskparser import use_args
from marshmallow import Schema, fields
from webargs.flaskparser import use_args



from app.schema.teams_schema import TeamSchema



teams_bp = Blueprint('teams_bp', __name__)

# Test Route
@teams_bp.route("/", methods=["GET"])
def index():
    return "Teams Blueprint Works!"

# Create Team
@teams_bp.route("/create", methods=["POST"])
@use_args(TeamSchema(), location="json")
def create_team(args):
  #using  Args making this code clean
   
    # name = args.get('name')
    # description = args.get('description', '')
    # admin_id = args.get('admin_id')

    # result, status = TeamBL.create_team(name, description, admin_id)
    result, status = TeamBL.create_team(**args)
    return jsonify(result), status



# Update Team

@teams_bp.route("/update", methods=["PUT"])
@use_args(TeamSchema(), location="json")
def update_team(args):
    result, status = TeamBL.update_team(args["id"], **args)
    return jsonify(result), status






# Get All Teams
@teams_bp.route("/all", methods=["GET"])
def get_all_teams():
    result = TeamBL.get_all_teams()
    return jsonify(result), 200



# Delete Team
@teams_bp.route('/delete/<int:team_id>', methods=['DELETE'])
def delete_team(team_id): 
    result, status = TeamBL.delete_team(team_id)
    return jsonify(result), status




# Remove User from Team
@teams_bp.route("/remove_user", methods=["DELETE"])
def remove_user_from_team():
    data = request.get_json()
    team_id = data.get("team_id")
    user_id = data.get("user_id")
    
    if not team_id or not user_id:
        return jsonify({"error": "Both team_id and user_id are required"}), 400

    result, status = TeamBL.remove_user_from_team(team_id, user_id)
    return jsonify(result), status

# Get All Users in a Team
@teams_bp.route("/<int:team_id>/users", methods=["GET"])
def get_users_in_team(team_id):
    result, status = TeamBL.get_users_in_team(team_id)
    return jsonify(result), status
    
    
    
    
    

# Get Team by ID
@teams_bp.route("/<int:id>", methods=["GET"])
def get_team_by_id(id):
    result, status = TeamBL.get_team_by_id(id)
    return jsonify(result), status
    
    
    
    
# Add User to Team    
@teams_bp.route("/add_user", methods=["POST"])
@use_args({"team_id": fields.Int(required=True), "user_id": fields.Int(required=True)}, location="json")
def add_user_to_team(args):
    result, status = TeamBL.add_user_to_team(args["team_id"], args["user_id"])
    return jsonify(result), status    