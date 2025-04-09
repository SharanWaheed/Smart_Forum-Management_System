from marshmallow import Schema, fields

class TaskSchema(Schema):
    id = fields.Int(required=False)
    title = fields.Str(required=True)
    description = fields.Str(allow_none=True)
    due_date = fields.Date(required=True)
    created_at = fields.DateTime(dump_only=True)


class TaskUpdateSchema(Schema):
    task_id = fields.Int(required=True)  # Ensure task_id is provided for updates
    title = fields.Str()
    description = fields.Str(allow_none=True)
    due_date = fields.Date()
    
task_schema = TaskSchema()  #Single task
tasks_schema = TaskSchema(many=True)  #  Multiple tasks
task_update_schema = TaskUpdateSchema()  # Task update schema


# class TaskSchema(Schema):
#     id = fields.Int(dump_only=True)
#     title = fields.Str(required=True, error_messages={"required": "Title is required"})
#     description = fields.Str(allow_none=True)
#     due_date = fields.Date(required=True, error_messages={"required": "Due Date is required"})
#     projects = fields.List(fields.Int(), allow_none=True)  # List of project IDs