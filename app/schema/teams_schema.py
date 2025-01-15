from marshmallow import Schema, fields, validate

class TeamSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1))
    description = fields.Str()
    admin_id = fields.Int(required=True)  # Ensure this field is defined and required
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    created_by = fields.Int()
