from flask import Blueprint, request, jsonify
from app.BL.teams_bl import TeamBL
from app.repo.teams_repo import TeamRepository
from app.schema.teams_schema import TeamSchema

teams_bp = Blueprint('teams_bp', __name__)
team_schema = TeamSchema()
team_list_schema = TeamSchema(many=True)

# Test Route
@teams_bp.route("/", methods=["GET"])
def index():
    return "Teams Blueprint Works!"

# Create Team
@teams_bp.route("/create", methods=["POST"])
def create_team():
    try:
        data = request.get_json()
        validated_data = team_schema.load(data)
        result, status = TeamBL.create_team(**validated_data)
        return jsonify(team_schema.dump(result) if status == 201 else result), status
    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500

# Get All Teams
@teams_bp.route("/all", methods=["GET"])
def get_all_teams():
    try:
        teams = TeamBL.get_all_teams()
        return jsonify(team_list_schema.dump(teams)), 200
    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500

# Get Team by ID
@teams_bp.route("/<int:id>", methods=["GET"])
def get_team_by_id(id):
    try:
        result, status = TeamBL.get_team_by_id(id)
        return jsonify(team_schema.dump(result) if status == 200 else result), status
    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500

# Update Team
@teams_bp.route("/update/<int:id>", methods=["PUT"])
def update_team(id):
    try:
        data = request.get_json()
        validated_data = team_schema.load(data)
        result, status = TeamBL.update_team(team_id=id, **validated_data)
        return jsonify(team_schema.dump(result) if status == 200 else result), status
    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500

# Delete Team
@teams_bp.route('/delete/<int:team_id>', methods=['DELETE'])
def delete_team_route(team_id):
    result = TeamRepository.delete_team(team_id)
    return jsonify(result), 200 if "successfully" in result["message"] else 404

# Add User to Team
@teams_bp.route("/<int:team_id>/add_user", methods=["POST"])
def add_user_to_team(team_id):
    try:
        data = request.get_json()
        user_id = data.get("user_id")
        if not user_id:
            return jsonify({"message": "user_id is required."}), 400
        result, status = TeamBL.add_user_to_team(team_id, user_id)
        return jsonify(result), status
    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500

# Remove User from Team
@teams_bp.route("/<int:team_id>/remove_user", methods=["DELETE"])
def remove_user_from_team(team_id):
    try:
        data = request.get_json()
        user_id = data.get("user_id")
        if not user_id:
            return jsonify({"message": "user_id is required."}), 400
        result, status = TeamBL.remove_user_from_team(team_id, user_id)
        return jsonify(result), status
    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500

# Get All Users in a Team
@teams_bp.route("/<int:team_id>/users", methods=["GET"])
def get_users_in_team(team_id):
    try:
        result, status = TeamBL.get_users_in_team(team_id)
        return jsonify(result), status
    except Exception as  e:
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500
    

    
