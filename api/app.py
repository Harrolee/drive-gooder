from dotenv import load_dotenv

load_dotenv(".env")

from flask import Flask, request
from flask import jsonify
from flask_httpauth import HTTPBasicAuth
from answer_question import answer_question_handler
from read_text import get_audio_for_text_handler
from request_models import QuestionTextRequestDto, QuestionTextRequestSchema
from request_models import (
    SummarizeRequestDto,
    SummarizeRequestSchema,
    ChunkTextRequestSchema,
    ChunkTextRequestDto,
    ReadTextRequestSchema,
    ReadTextRequestDto,
)
import functools
from marshmallow import Schema, ValidationError
from os import environ
from werkzeug.security import generate_password_hash, check_password_hash
from summarize import summarize_handler
from chunk_text import chunk_text_handler
from typing import IO, Dict


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


@app.route("/", methods=["GET"])
@auth.login_required
def healthCheck():
    return "", 204


@app.route("/summarize", methods=["POST"])
@auth.verify_password
@validate_request_json(SummarizeRequestSchema())
def summarize(data: SummarizeRequestDto):
    return summarize_handler(data), 200


@app.route("/split", methods=["POST"])
@auth.verify_password
@validate_request_json(ChunkTextRequestSchema())
def chunk_text(data: ChunkTextRequestDto):
    return chunk_text_handler(data), 200


@app.route("/read", methods=["POST"])
@auth.verify_password
@validate_request_json(ReadTextRequestSchema())
def get_audio_for_text(data: ReadTextRequestDto):
    return get_audio_for_text_handler(data), 200


@app.route("/ask", methods=["POST"])
@auth.verify_password
@validate_file_on_request("question.wav")
@validate_request_form(QuestionTextRequestSchema())
def answer_question(file_data: IO, data: QuestionTextRequestDto):
    return answer_question_handler(file_data, data), 200


if __name__ == "__main__":
    app.run(port=5003)
