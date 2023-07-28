from marshmallow import Schema, fields, post_load

class LoginRequestSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)

    @post_load
    def make_user(self, data, **kwargs):
        return LoginRequestDto(**data)
    
class LoginRequestDto():
    def __init__(self, username, password) -> None:
        self.username = username
        self.password = password


class UserResponseSchema(Schema):
    id = fields.Str()
    username = fields.Str()
    first_name = fields.Str()
    last_name = fields.Str()
    email = fields.Str()