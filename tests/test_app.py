import time
from flask.testing import FlaskClient
import pytest
from fmapi.app import app


@pytest.fixture
def client():
    return app.test_client()


def test_index_route(client: FlaskClient) -> None:
    response = client.get("/")
    assert response.status_code == 401


def test_register_route(client: FlaskClient) -> None:
    now = str(time.time()).replace(".", "")
    response = client.post("/register", json={
        "name": "maria", "email": f"m{now}@ma.com", "password": "ma12"
    })
    assert response.status_code == 201


def test_login_route(client: FlaskClient) -> None:
    now = str(time.time()).replace(".", "")
    register_data = {"name": "maria", "email": f"m{now}@ma.com", "password": "ma12"}
    login_data = {"email": f"m{now}@ma.com", "password": "ma12"}

    # register a new login for login methods tests below
    response = client.post("/register", json=register_data)
    assert response.status_code == 201

    # test post method
    response = client.post("/login", json=login_data)
    assert response.status_code == 200

    # test get method
    response = client.get("/login", json=login_data)
    assert response.status_code == 405

    # test patch method
    response = client.patch("/login", json=login_data)
    assert response.status_code == 405

    # test put method
    response = client.put("/login", json=login_data)
    assert response.status_code == 405

    # test delete method
    response = client.delete("/login", json=login_data)
    assert response.status_code == 405


def test_main_flow(client: FlaskClient) -> None:
    # register a new user
    now = str(time.time()).replace(".", "")
    login = f"{now}@ma.com"
    response = client.post("/register", json={
        "name": "maria", "email": login, "password": "ma12"
    })
    assert response.status_code == 201

    # login to get access_token
    response = client.post("/login", json={
        "email": login, "password": "ma12"
    })

    access_token = response.json.get("access_token")

    assert response.status_code == 200
    assert access_token is not None

    # send access_token to index route to get full parameters of todo list endpoint
    payload = {}
    response = client.get("/", headers={"Authorization": f"Bearer {access_token}"}, data=payload)

    assert response.status_code == 200

    # send access_token to index route to get only id and title parameters of todo list endpoint
    payload = {"only_id_title": 1}
    response = client.post("/", headers={"Authorization": f"Bearer {access_token}"}, data=payload)

    assert response.status_code == 200
