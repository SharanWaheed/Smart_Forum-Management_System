from marshmallow import Schema, fields

class AllocationSchema(Schema):
    id = fields.Int(dump_only=True)
    project_id = fields.Int(required=False, allow_none=True)
    task_id = fields.Int(required=False, allow_none=True)
    user_id = fields.Int(required=True)
    status = fields.Str(required=True)
    assigned_at = fields.DateTime(dump_only=True)
