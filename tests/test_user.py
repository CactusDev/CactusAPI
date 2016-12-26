import pytest

user_creation_data = {
    "service": "beam",
    "userId": 24228,
    "password": "foo",
    "token": "paradigmshift3d"
}


def test_user(client):
    url = "/api/v1/user/ParadigmShift3d"
    user_data = user_creation(client, url)
    user_single(client, user_data, url)
    user_removal(client, user_data, url)


def user_creation(client, url):
    # Valid user creation
    user = client.post(url, data=user_creation_data)
    user_data = user.json
    assert "data" in user_data
    assert "attributes" in user_data["data"]
    assert "id" in user_data["data"]

    return user_data


def user_single(client, user_data, url):
    user = client.get(url)
    user_single_data = user.json
    assert "data" in user_single_data
    assert "attributes" in user_single_data["data"]
    assert "id" in user_single_data["data"]
    assert user_single_data["data"]["id"] == user_data["data"]["id"]


def user_removal(client, user_data, url):
    user = client.delete(url)
    deletion_data = user.json
    assert "meta" in deletion_data
    assert "deleted" in deletion_data["meta"]
    assert deletion_data["meta"]["deleted"][0] == user_data["data"]["id"]
