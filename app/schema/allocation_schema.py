from marshmallow import Schema, fields

class AllocationSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True, error_messages={"required": "user_id is required"})
    task_id = fields.Int(required=False, allow_none=True)  #Optional
    project_id = fields.Int(required=False, allow_none=True)
    status = fields.Str(allow_none=True, load_default=None)
    assigned_at = fields.DateTime(dump_only=True)

class UpdateAllocationSchema(Schema):
    allocation_id = fields.Int(required=True, error_messages={"required": "allocation_id is required"})
    project_id = fields.Int(allow_none=True, missing=None)  # Allow null & missing values
    task_id = fields.Int(allow_none=True, missing=None)
    user_id = fields.Int(allow_none=True, missing=None)
    status = fields.Str(allow_none=True, load_default=None)