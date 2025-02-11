from marshmallow import Schema, fields, validate
from app.schema.teams_schema import TeamSchema  # Import the TeamSchema for nested serialization

class UserSchema(Schema):
    id = fields.Int(required=False)
    name = fields.Str(required=False)  # Optional for update
    email = fields.Email(required=False)  # Optional for update
    password = fields.Str(required=False, load_only=True)  # Optional for update
    role = fields.Str(required=False, missing="member")  # Default role for new users
    is_active = fields.Boolean(required=False, missing=True)
    phone = fields.Str(allow_none=True)
    profile_picture = fields.Str(allow_none=True)
    teams = fields.List(
        fields.Nested(TeamSchema, only=("id", "name", "description")), 
        required=False, dump_only=True
    )  # Teams are dump-only by default
