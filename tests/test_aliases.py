"""Tests the alias endpoint of the API"""
import json
import pytest


class TestAliases:
    """Tests the social endpoint of the API"""
    creation_data = {
        "test": {
            "commandName": "foo",
            "arguments": [
                {
                    "type": "text",
                    "data": "Spam spam! Beautiful spam!",
                    "text": "Spam spam! Beautiful spam!",
                }
            ]
        },
        "taco": {
            "commandName": "bar",
            "arguments": []
        }
    }
    url = "/api/v1/user/paradigmshift3d/alias"

    def test_create(self, client, api_auth, command_data):
        """Valid social service creation"""
        name = "test"
        cmd_name = "foo"
        cmd = client.patch("/api/v1/user/paradigmshift3d/command/" + cmd_name,
                           data=json.dumps(command_data[cmd_name]),
                           content_type="application/json",
                           headers=api_auth)

        # The command was created successfully, so we can continue
        assert cmd.status_code == 201
        created_id = json.loads(cmd.data.decode())["data"]["id"]

        alias = client.patch(self.url + '/' + name,
                             data=json.dumps(self.creation_data[name]),
                             content_type="application/json",
                             headers=api_auth)
        data = json.loads(alias.data.decode())
        assert alias.status_code == 201
        # FIXME: This needs to be able to test for alias instead of aliases
        assert data["data"]["type"] == "aliases"
        data = data["data"]

        assert data["attributes"]["command"]["count"] == 0
        assert data["attributes"]["command"]["token"] == "paradigmshift3d"
        assert data["attributes"]["command"].get("enabled", False)
        assert data["attributes"]["command"]["id"] == created_id

        del data["attributes"]["command"]["count"]
        del data["attributes"]["command"]["token"]
        del data["attributes"]["command"]["enabled"]
        del data["attributes"]["command"]["id"]

        assert data["attributes"][
            "arguments"] == self.creation_data[name]["arguments"]
        assert data["attributes"][
            "command"] == command_data[cmd_name]

    def test_single(self, client, api_auth, command_data):
        """A test that does stuff, namely checking if stuff == other stuff"""
        name = "taco"
        cmd_name = "bar"
        cmd = client.patch("/api/v1/user/paradigmshift3d/command/" + cmd_name,
                           data=json.dumps(command_data[cmd_name]),
                           content_type="application/json",
                           headers=api_auth)
        # The command was created successfully, so we can continue
        assert cmd.status_code == 201

        alias = client.patch(self.url + '/' + name,
                             data=json.dumps(self.creation_data[name]),
                             content_type="application/json",
                             headers=api_auth)
        created_id = json.loads(alias.data.decode())["data"]["id"]
        assert alias.status_code == 201

        alias = client.get(self.url + '/' + name)
        data = json.loads(alias.data.decode())["data"]

        assert data["id"] == created_id
        assert data["attributes"]["command"]["count"] == 0
        assert data["attributes"]["command"]["token"] == "paradigmshift3d"
        assert data["attributes"]["command"].get("enabled", False)

        del data["attributes"]["command"]["count"]
        del data["attributes"]["command"]["token"]
        del data["attributes"]["command"]["enabled"]
        del data["attributes"]["command"]["id"]

        assert data["attributes"][
            "command"] == command_data[cmd_name]
        assert data["attributes"]["token"] == "paradigmshift3d"
        assert data["attributes"]["commandName"] == cmd_name
        assert data["attributes"][
            "arguments"] == self.creation_data[name]["arguments"]

        assert (client.delete(self.url + '/' + name,
                              headers=api_auth)).status_code == 200

    def test_delete(self, client, api_auth):
        """Test to see if the services are being removed properly"""
        name = "taco"
        alias = client.patch(self.url + '/' + name,
                             data=json.dumps(self.creation_data[name]),
                             content_type="application/json",
                             headers=api_auth)
        created_id = json.loads(alias.data.decode())["data"]["id"]
        assert alias.status_code == 201

        deleted = client.delete(self.url + '/' + name, headers=api_auth)
        assert deleted.status_code == 200
        data = json.loads(deleted.data.decode())
        assert len(data["meta"]["deleted"]) == 1
        assert data["meta"]["deleted"][0] == created_id

        assert (client.delete("/api/v1/user/paradigmshift3d/command/foo",
                              headers=api_auth)).status_code == 200
        assert (client.delete("/api/v1/user/paradigmshift3d/command/bar",
                              headers=api_auth)).status_code == 200
