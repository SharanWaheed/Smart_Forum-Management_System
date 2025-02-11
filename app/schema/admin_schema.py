from marshmallow import Schema, fields, post_load, pre_load, validate
from app.models.admin_model import Admin 

from werkzeug.security import generate_password_hash

class AdminSchema(Schema):
    id = fields.Int(required=False)
    name = fields.Str(required=True, validate=validate.Length(min=1))
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True, validate=validate.Length(min=6))
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True) 
    
    
    @pre_load
    def process_input_data(self, data, **kwargs):
        """ This is executed before the data is loaded into the schema """
        # Example: Normalize email (convert to lowercase)
        if 'email' in data:
            data['email'] = data['email'].lower()
        return data
    
    @post_load
    def hash_password(self, data, **kwargs):
        """ Hash the password after data is loaded into the schema """
        if 'password' in data:
            data['password'] = generate_password_hash(data['password'])
        return data