from json import dumps, loads
import pytest


class TestQuotes:
    creation_data = {
        "foo": {
            "name": "foo",
            "response": {
                "role": 0,
                "action": False,
                "target": None,
                "user": "",
                "message": [
                    {
                        "type": "text",
                        "data": "lol!",
                        "text": "lol!"
                    }
                ]
            }
        },
        "bar": {
            "name": "bar",
            "response": {
                "role": 0,
                "action": False,
                "target": None,
                "user": "",
                "message": [
                    {
                        "type": "emoji",
                        "data": "smile",
                        "text": ":)"
                    },
                    {
                        "type": "link",
                        "data": "https://google.com",
                        "text": "google.com"
                    }
                ]
            }
        }
    }
    url = "/api/v1/user/paradigmshift3d/command"
    data = {}

    def test_create(self, client, api_auth):
        """Valid command creation"""
        # Get data from the creation_data dict
        name = "foo"
        cmd = client.patch(self.url + "/" + name,
                           data=dumps(self.creation_data[name]),
                           content_type="application/json",
                           headers=api_auth)

        data = loads(cmd.data.decode())["data"]
        assert data["attributes"]["count"] == 0
        del data["attributes"]["count"]

        assert "attributes" in data
        assert "id" in data
        assert data["attributes"]["token"] == "paradigmshift3d"
        assert data["attributes"]["enabled"] is True
        assert data["attributes"]["name"] == name
        assert data["type"] == "command"

        # The submitted data does not have these keys and we already asserted
        # them, so add them so the final test can complete
        self.creation_data[name]["token"] = data["attributes"]["token"]
        self.creation_data[name]["enabled"] = data["attributes"]["enabled"]

        assert self.creation_data[name] == data["attributes"]

    def test_single(self, client):
        """Get a single user object and see if it matches (it should)"""
        name = "foo"
        cmd = client.get(self.url + "/" + self.creation_data[name]["name"])

        cmd_data = loads(cmd.data.decode())["data"]
        assert cmd_data["attributes"]["count"] == 0
        del cmd_data["attributes"]["count"]

        assert cmd_data["attributes"] == self.creation_data[name]

    def test_all(self, client, api_auth):
        # Create the second command
        name = "bar"
        cmd = client.patch(
            self.url + "/" + name,
            data=dumps(self.creation_data[name]),
            content_type="application/json",
            headers=api_auth
        )
        cmd_create_data = cmd.json["data"]

        assert "attributes" in cmd_create_data
        assert "id" in cmd_create_data
        assert cmd_create_data["attributes"]["token"] == "paradigmshift3d"
        assert cmd_create_data["attributes"]["enabled"] is True
        assert cmd_create_data["attributes"]["name"] == name
        assert cmd_create_data["type"] == "command"

        # These have already been asserted, so go ahead and remove them
        del cmd_create_data["attributes"]["count"]
        del cmd_create_data["attributes"]["enabled"]
        del cmd_create_data["attributes"]["token"]

        assert cmd_create_data["attributes"] == self.creation_data[name]

        cmd = client.get(self.url)
        cmd_all_data = cmd.json["data"]
        assert len(cmd_all_data) == 2

        returned_cmds = [cmd["attributes"]["name"] for cmd in cmd_all_data]

        for name in self.creation_data.keys():
            if name not in returned_cmds:
                raise AssertionError(
                    "Command {name} was not returned by API!".format(name=name)
                )

    def test_edit(self, client, api_auth):
        edit_data = {
            "enabled": False,
            "response": {
                "message": [
                    {
                        "type": "emoji",
                        "data": "smile",
                        "text": ":)"
                    }
                ]
            }
        }
        edit_name = "foo"

        cmd = client.patch(
            self.url + "/" + edit_name,
            data=dumps(edit_data),
            content_type="application/json",
            headers=api_auth
        )

        data = loads(cmd.data.decode())

        assert data["meta"]["edited"] is True
        assert data["data"]["attributes"]["enabled"] is False
        assert data["data"]["attributes"][
            "response"]["message"] == edit_data["response"]["message"]

    def test_removal(self, client, api_auth):
        """Remove a command and see if it matches"""
        # Using the quote ID from the first created quote
        for name in self.creation_data.keys():
            _ = client.delete(self.url + "/" + name, headers=api_auth)

        # Create command to delete
        name = "foo"
        cmd = client.patch(self.url + "/" + name,
                           data=dumps(self.creation_data[name]),
                           content_type="application/json",
                           headers=api_auth)

        created_id = loads(cmd.data.decode())["data"]["id"]

        deleted = client.delete(self.url + "/" + name, headers=api_auth)
        deletion_data = loads(deleted.data.decode())

        assert deletion_data["meta"]["deleted"]["command"][0] == created_id
