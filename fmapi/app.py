from flask import jsonify, request, json
from flask_httpauth import HTTPTokenAuth
from werkzeug.exceptions import HTTPException

from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from fmapi.create_app import create_app
from fmapi.models import User
from fmapi.logger import Logger

import fmapi.database as database
import requests

API_URL = "https://jsonplaceholder.typicode.com/todos"
app = create_app()
token_serializer = Serializer(app.config["SECRET_KEY"], expires_in=app.config["AUTH_TOKEN_EXPIRES_IN"])
auth = HTTPTokenAuth("Bearer")
logger = Logger.get_logger(log_name="fmapi_logger", is_file_handler=app.config["LOG_TO_FILE"])


@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({"error": {"reason": e.description}})
    response.content_type = "application/json"
    return response


@auth.verify_token
def verify_token(token):
    try:
        data = token_serializer.loads(token)
    except:  # noqa: E722
        return False
    if "email" in data:
        return data["email"]


@app.route("/register", methods=["POST"])
def register():
    """Register a new user and store it in database."""
    data = request.json
    email = data.get("email")

    email_exist = User.query.filter_by(email=email).first()
    if email_exist:
        return jsonify(message="Email already exists."), 409
    else:
        database.add_instance(
            model=User,
            name=data.get("name"),
            email=email,
            password=generate_password_hash(data.get("password"))
        )
        return jsonify(message="User created successfully."), 201


@app.route("/login", methods=["POST"])
def login():
    """Login if it is a valid user.

    Possible returns:
    successful: {"access_token": <access_token>, "message": "Login succeeded!"}
    unsuccessful: {"message": "Bad email or password"}
    """
    data = request.json
    email = data.get("email")

    valid_user = User.query.filter_by(email=email).first()
    if valid_user and check_password_hash(valid_user.password, data.get("password")):
        access_token = token_serializer.dumps({"email": email}).decode("utf-8")
        return jsonify(message="Login succeeded!", access_token=access_token)
    else:
        return jsonify(message="Bad email or password"), 401


@app.route("/", methods=["GET", "POST"])
@auth.login_required
def get_todos():
    """Returns the first five items from todos endpoint."""
    try:
        response = requests.get(url=API_URL)
        response.raise_for_status()
    except requests.exceptions.RequestException as exceptions:
        logger.info(msg=f"{exceptions}")
        return {"error": {"reason": response.reason}}, response.status_code

    data = response.json()
    logger.info(msg=f"{response.status_code}:{response.raw.info()}")

    if request.is_json and request.json.get("only_id_title"):
        # returns only id and title parameters
        return {"data": [{"id": item["id"], "title": item["title"]} for item in data[:5]]}

    # returns all parameters available (completed, id, title, userId)
    return {"data": data[:5]}


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
