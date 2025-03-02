from marshmallow import Schema, fields

class TaskSchema(Schema):
    id = fields.Int(required=False)
    title = fields.Str(required=True)
    description = fields.Str(allow_none=True)
    due_date = fields.Date(required=True)
    created_at = fields.DateTime(dump_only=True)

task_schema = TaskSchema()  #Single task
tasks_schema = TaskSchema(many=True)  #  Multiple tasks
