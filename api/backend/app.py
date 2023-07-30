from flask import Flask, request
from flask_cors import CORS
from flask import jsonify
from flask_httpauth import HTTPBasicAuth
# Must import env vars before import modules that use env vars
from dotenv import load_dotenv  # noqa
load_dotenv(".env")  # noqa
from backend.handlers.answer_question import answer_question_handler
from backend.handlers.read_text import get_audio_for_text_handler
from backend.request_models import QuestionTextRequestDto, QuestionTextRequestSchema
from backend.request_models import (
    SummarizeRequestDto,
    SummarizeRequestSchema,
    ChunkTextRequestSchema,
    ChunkTextRequestDto,
    ReadTextRequestSchema,
    ReadTextRequestDto,
)
from typing import IO, Dict
from backend.handlers.chunk_text import chunk_text_handler
from backend.handlers.summarize import summarize_handler
from werkzeug.security import generate_password_hash, check_password_hash
from os import environ
from marshmallow import Schema, ValidationError
import functools


app = Flask(__name__)
CORS(app)
auth = HTTPBasicAuth()

basic_auth_username = environ["BASIC_AUTH_USERNAME"]
basic_auth_password = generate_password_hash(environ["BASIC_AUTH_PASSWORD"])


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


def validate_request_form(schema_obj: Schema):
    def Inner(func):
        @functools.wraps(func)
        def wrap_request_validation(*args, **kwargs):
            try:
                request_data = schema_obj.load(request.form)
                return func(*args, **kwargs, data=request_data)
            except ValidationError as err:
                return str(err), 400

        return wrap_request_validation

    return Inner


def validate_file_on_request(file_name: str):
    def Inner(func):
        @functools.wraps(func)
        def wrap_request_validation(*args, **kwargs):
            if file_name in request.files:
                return func(*args, **kwargs, file_data=request.files[file_name])
            return f"{file_name} file not present on request", 400

        return wrap_request_validation

    return Inner


@auth.verify_password
def verify_password(username, password):
    if username != basic_auth_username:
        return False
    return check_password_hash(basic_auth_password, password)


@app.route("/authenticate", methods=["POST"])
@auth.login_required
def authenticate():
    return "", 204


@app.route("/", methods=["GET"])
def healthCheck():
    return "", 204


@app.route("/summarize", methods=["POST"])
@auth.login_required
@validate_request_json(SummarizeRequestSchema())
def summarize(data: SummarizeRequestDto):
    return summarize_handler(data), 200


@app.route("/split", methods=["POST"])
@auth.login_required
@validate_request_json(ChunkTextRequestSchema())
def chunk_text(data: ChunkTextRequestDto):
    return chunk_text_handler(data), 200


@app.route("/read", methods=["POST"])
@auth.login_required
@validate_request_json(ReadTextRequestSchema())
def get_audio_for_text(data: ReadTextRequestDto):
    return get_audio_for_text_handler(data), 200


@app.route("/ask", methods=["POST"])
@auth.login_required
@validate_file_on_request("question.wav")
@validate_request_form(QuestionTextRequestSchema())
def answer_question(file_data: IO, data: QuestionTextRequestDto):
    return answer_question_handler(file_data, data), 200


def start():
    app.run(port=5003)
