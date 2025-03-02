from flask import Blueprint, jsonify
from webargs.flaskparser import use_args
from marshmallow import Schema, fields
from app.BL.allocation_bl import AllocationBL  # ✅ Import at the top
from app.schema.allocation_schema import AllocationSchema

allocation_bp = Blueprint('allocation', __name__)



# Routes with validation
@allocation_bp.route('/allocate', methods=['POST'])
@use_args(AllocationSchema(), location="json")
def allocate_user(args):
    result, status_code = AllocationBL.allocate_user(  # ✅ Now correctly structured
        args["project_id"], args["task_id"], args["user_id"], args["status"]
    )
    return jsonify(result), status_code  # ✅ Correct JSON response


@allocation_bp.route('/update_allocation', methods=['PUT'])  #  No URL param
@use_args(AllocationSchema(), location="json")
def update_allocation(args):
    result, status_code = AllocationBL.update_allocation(args["allocation_id"], args["status"])
    return jsonify(result), status_code

@allocation_bp.route('/deallocate', methods=['DELETE'])
@use_args(AllocationSchema(), location="json")
def deallocate_user(args):
    result, status_code = AllocationBL.deallocate_user(args["allocation_id"])
    return jsonify(result), status_code

@allocation_bp.route('/allocations', methods=['GET'])
def get_allocations():
    allocations = AllocationBL.get_allocations()
    return jsonify(allocations), 200
