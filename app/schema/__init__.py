from app.schema.project_schema import ProjectSchema
from app.schema.task_schema import TaskSchema  # ✅ Import TaskSchema

from marshmallow import Schema, fields

project_schema = ProjectSchema()
projects_schema = ProjectSchema(many=True)  #   Add this if missing


#  Task Schema Instances
task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)