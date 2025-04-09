from flask import Blueprint, jsonify, request
from webargs.flaskparser import use_args
from app.BL.allocation_bl import AllocationBL
from app.schema.allocation_schema import AllocationSchema, UpdateAllocationSchema

allocation_bp = Blueprint('allocation', __name__)

@allocation_bp.route('/allocate', methods=['POST'])
@use_args(AllocationSchema(), location="json")
def allocate_user(args):
    result, status_code = AllocationBL.allocate_user(**args)
    return jsonify(result), status_code


@allocation_bp.route('/update_allocation', methods=['PUT'])
@use_args(UpdateAllocationSchema(), location="json")
def update_allocation(args):
    print("Received payload:", args)  # Debug the actual data received
    return AllocationBL.update_allocation(args)


@allocation_bp.route('/deallocate', methods=['DELETE'])
@use_args(UpdateAllocationSchema(only=("allocation_id",)), location="json")
def deallocate_user(args):
    result, status_code = AllocationBL.deallocate_user(args["allocation_id"])
    return jsonify(result), status_code



@allocation_bp.route('/allocations', methods=['GET'])
def get_allocations():
    result, status_code = AllocationBL.get_allocations()
    return jsonify(result), status_code
