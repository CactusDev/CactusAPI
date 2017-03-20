import pytest
import json


class TestUsers:
    creation_data = {
        "service": "beam",
        "userId": 24228,
        "password": "foo",
        "token": "paradigmshift3d"
    }
    url = "/api/v1/user/ParadigmShift3d"

    def test_create(self, client, api_auth):
        """Valid user creation"""
        user = client.post(self.url, data=self.creation_data, headers=api_auth)
        data = json.loads(user.data.decode())["data"]

        assert data["type"] == "user"
        comparison_data = {
            **{k: v for k, v in self.creation_data.items() if k != "password"},
            "userName": "ParadigmShift3d"
        }
        assert data["attributes"] == comparison_data

        # Delete the user so we have a clean environment to work in
        client.delete(self.url, headers=api_auth)

    def test_single(self, client, api_auth):
        """Get a single user object and see if it matches (it should)"""
        user = client.post(self.url, data=self.creation_data, headers=api_auth)
        creation_data = json.loads(user.data.decode())["data"]

        comparison_data = {
            **{k: v for k, v in self.creation_data.items() if k != "password"},
            "userName": "ParadigmShift3d"
        }

        user = client.get(self.url)
        single_data = json.loads(user.data.decode())["data"]
        assert single_data["id"] == creation_data["id"]
        assert single_data["attributes"] == comparison_data

        # Clean up the DB
        client.delete(self.url, headers=api_auth)

    def test_removal(self, client, api_auth):
        """Remove a user and see if it matches"""
        user = client.post(
            self.url, data=self.creation_data, headers=api_auth)
        data = json.loads(user.data.decode())["data"]

        user = client.delete(self.url, headers=api_auth)
        deletion_data = json.loads(user.data.decode())
        assert len(deletion_data["meta"]["deleted"]) == 1
        assert deletion_data["meta"]["deleted"][0] == data["id"]
