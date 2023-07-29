from flask import Flask, request
from flask import jsonify
from request_models import LoginRequestSchema, LoginRequestDto
import functools
from marshmallow import Schema, ValidationError

app = Flask(__name__)


def validate_request_json(schema_obj: Schema):
    def Inner(func):
        @functools.wraps(func)
        def wrap_request_validation(*args, **kwargs):
            try:
                request_data = schema_obj.load(request.json)
                return func(*args, **kwargs, data=request_data)
            except ValidationError as err:
                return str(err), 400

        return wrap_request_validation

    return Inner


@app.route("/", methods=["GET"])
def healthCheck():
    return "", 204


@app.route("/login", methods=["POST"])
@validate_request_json(LoginRequestSchema())
def login(data: LoginRequestDto):
    return "", 200


if __name__ == "__main__":
    app.run(port=5003)
