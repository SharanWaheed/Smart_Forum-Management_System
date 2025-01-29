from marshmallow import Schema, fields, validate
from app.schema.teams_schema import TeamSchema  # Import the TeamSchema for nested serialization

class UserSchema(Schema):
    id = fields.Int(dump_only=True)  # User ID is only for responses
    name = fields.Str(required=True, validate=validate.Length(min=1))  # Name is required, min 1 character
    email = fields.Email(required=True)  # Validate email format
    password = fields.Str(required=True, load_only=True, validate=validate.Length(min=6))  # Password must be at least 6 characters
    role = fields.Str(required=False, missing="member")  # Default role is 'member'
    is_active = fields.Boolean(required=False, missing=True)  # Default to active
    phone = fields.Str(validate=validate.Length(max=15), allow_none=True)  # Optional phone, max length 15
    profile_picture = fields.Str(allow_none=True)  # Optional profile picture
    teams = fields.List(
        fields.Nested(TeamSchema, only=("id", "name", "description")), 
        required=False, dump_only=True
    )  # Teams are dump-only by defaultare dump-only by default