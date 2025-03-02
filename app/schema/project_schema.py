from marshmallow import Schema, fields

class ProjectSchema(Schema):
    id = fields.Int(dump_only=False)
    name = fields.Str(required=True)
    description = fields.Str(allow_none=True)
    start_date = fields.Date(required=True)  # ✅ Added start_date
    end_date = fields.Date(required=True)  # ✅ Added end_date
    created_at = fields.DateTime(dump_only=True)

project_schema = ProjectSchema()  # Instance for a single project
projects_schema = ProjectSchema(many=True)  # Instance for multiple projects
