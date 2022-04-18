from fmapi.app import create_app


def test_configs():
    app = create_app()
    assert app.config["SECRET_KEY"] != ""
    assert app.config["AUTH_TOKEN_EXPIRES_IN"] == 1200
    assert app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] is False

