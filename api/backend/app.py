import sqlite3
from flask import Flask, redirect, request, url_for, jsonify
from flask_cors import CORS
# from flask_httpauth import HTTPBasicAuth
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
# Internal imports
from backend.data.db import init_db_command
from backend.data.user import User
from typing import IO, Dict
from backend.handlers.chunk_text import chunk_text_handler
from backend.handlers.summarize import summarize_handler
# from werkzeug.security import generate_password_hash, check_password_hash
from os import environ, urandom
from marshmallow import Schema, ValidationError
import functools
import json
# Third-party libraries
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)


from oauthlib.oauth2 import WebApplicationClient
import requests

app = Flask(__name__)
app.secret_key = urandom(24)
CORS(app)
# auth = HTTPBasicAuth()

# basic_auth_username = environ["BASIC_AUTH_USERNAME"]
# basic_auth_password = generate_password_hash(environ["BASIC_AUTH_PASSWORD"])

GOOGLE_CLIENT_ID = environ["GOOGLE_CLIENT_ID"]
GOOGLE_CLIENT_SECRET = environ["GOOGLE_CLIENT_SECRET"]
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)


# User session management setup
# https://flask-login.readthedocs.io/en/latest
login_manager = LoginManager()
login_manager.init_app(app)

def setup_db():
    # Naive database setup
    try:
        init_db_command()
    except sqlite3.OperationalError:
        # Assume it's already been created
        pass

# OAuth 2 client setup
client = WebApplicationClient(GOOGLE_CLIENT_ID)

# Flask-Login helper to retrieve a user from our db
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


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


# @auth.verify_password
# def verify_password(username, password):
#     if username != basic_auth_username:
#         return False
#     return check_password_hash(basic_auth_password, password)

def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()


#########
# following this tutorial: https://realpython.com/flask-google-login/
@app.route("/temp-homepage")
def index():
    setup_db()
    if current_user.is_authenticated:
        return (
            "<p>Hello, {}! You're logged in! Email: {}</p>"
            "<div><p>Google Profile Picture:</p>"
            '<img src="{}" alt="Google profile pic"></img></div>'
            '<a class="button" href="/logout">Logout</a>'.format(
                current_user.name, current_user.email, current_user.profile_pic
            )
        )
    else:
        return '<a class="button" href="/login">Google Login</a>'
    

@app.route("/login")
def login():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)



@app.route("/login/callback")
def callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")

    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    # Prepare and send a request to get tokens! Yay tokens!
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))


    # Now that you have tokens (yay) let's find and hit the URL
    # from Google that gives you the user's profile information,
    # including their Google profile image and email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    # You want to make sure their email is verified.
    # The user authenticated with Google, authorized your
    # app, and now you've verified their email through Google!
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400

    # Create a user in your db with the information provided
    # by Google
    user = User(
        id_=unique_id, name=users_name, email=users_email, profile_pic=picture
    )

    # Doesn't exist? Add it to the database.
    if not User.get(unique_id):
        User.create(unique_id, users_name, users_email, picture)

    # Begin user session by logging the user in
    login_user(user)

    # Send user back to homepage
    return redirect(url_for("index"))


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

#########

@app.route("/authenticate", methods=["POST"])
@login_required
def authenticate():
    return "", 204


@app.route("/", methods=["GET"])
def healthCheck():
    return "", 204


@app.route("/summarize", methods=["POST"])
@login_required
@validate_request_json(SummarizeRequestSchema())
def summarize(data: SummarizeRequestDto):
    return summarize_handler(data), 200


@app.route("/split", methods=["POST"])
@login_required
@validate_request_json(ChunkTextRequestSchema())
def chunk_text(data: ChunkTextRequestDto):
    return chunk_text_handler(data), 200


@app.route("/read", methods=["POST"])
@login_required
@validate_request_json(ReadTextRequestSchema())
def get_audio_for_text(data: ReadTextRequestDto):
    return get_audio_for_text_handler(data), 200


@app.route("/ask", methods=["POST"])
@login_required
@validate_file_on_request("question.wav")
@validate_request_form(QuestionTextRequestSchema())
def answer_question(file_data: IO, data: QuestionTextRequestDto):
    return answer_question_handler(file_data, data), 200


def start():
    app.run(port=5003,ssl_context="adhoc")