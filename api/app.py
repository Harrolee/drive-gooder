from flask import Flask, request
from flask import jsonify
from flask_httpauth import HTTPBasicAuth
from request_models import LoginRequestSchema, LoginRequestDto, SummarizeRequestDto, SummarizeRequestSchema
import functools
from marshmallow import Schema, ValidationError
from os import environ
from werkzeug.security import generate_password_hash, check_password_hash

from dotenv import load_dotenv

load_dotenv(".env")

from summarize import summarize_handler

app = Flask(__name__)
auth = HTTPBasicAuth()

basic_auth_username = environ["BASIC_AUTH_USERNAME"]
basic_auth_password = generate_password_hash(environ["BASIC_AUTH_PASSWORD"])


def validate_request_json(schema_obj: Schema):
    def Inner(func):
        @functools.wraps(func)
        def wrap_request_validation(*args, **kwargs):
            try:
                request_data = schema_obj.load(request.json)
                print(args, kwargs)
                return func(*args, **kwargs, data=request_data)
            except ValidationError as err:
                return str(err), 400

        return wrap_request_validation

    return Inner


@auth.verify_password
def verify_password(username, password):
    if username != basic_auth_username:
        return False
    return check_password_hash(basic_auth_password, password)


@app.route("/", methods=["GET"])
@auth.login_required
def healthCheck():
    return "", 204


@app.route("/login", methods=["POST"])
@auth.login_required
@validate_request_json(LoginRequestSchema())
def login(data: LoginRequestDto):
    return "", 200


@app.route("/summarize", methods=["POST"])
@auth.verify_password
@validate_request_json(SummarizeRequestSchema())
def summarize(data: SummarizeRequestDto):
    return summarize_handler(data), 200


if __name__ == "__main__":
    app.run(port=5003)
