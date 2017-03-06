from json import dumps, loads
import pytest


class TestQuotes:
    creation_data = [
        {
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
        {
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
    ]
    url = "/api/v1/user/paradigmshift3d/command"
    data = {}

    def test_create(self, client, api_auth):
        """Valid command creation"""
        # Get data from the creation_data dict
        name = self.creation_data[0]["name"]
        cmd = client.patch(self.url + "/" + name,
                           data=dumps(self.creation_data[0]),
                           content_type="application/json",
                           headers=api_auth)

        data = loads(cmd.data.decode())["data"]

        assert "attributes" in data
        assert "id" in data
        assert data["attributes"]["token"] == "paradigmshift3d"
        assert data["attributes"]["enabled"] is True
        assert data["attributes"]["name"] == name
        assert data["type"] == "command"

        # The submitted data does not have these keys and we already asserted
        # them, so add them so the final test can complete
        self.creation_data[0]["token"] = data["attributes"]["token"]
        self.creation_data[0]["enabled"] = data["attributes"]["enabled"]

        assert self.creation_data[0] == data["attributes"]
    #
    # def test_single(self, client):
    #     """Get a single user object and see if it matches (it should)"""
    #     cmd = client.get(self.url + "/" + self.data["attributes"]["name"])
    #     cmd_single_data = cmd.json["data"]
    #
    #     assert cmd_single_data["attributes"] == self.data["attributes"]
    #     assert cmd_single_data["id"] == self.data["id"]
    #
    # def test_all(self, client):
    #     # Create the second command
    #     name = self.creation_data[1]["name"]
    #     cmd = client.patch(
    #         self.url + "/" + name,
    #         data=dumps(self.creation_data[1]),
    #         content_type="application/json"
    #     )
    #     cmd_create_data = cmd.json["data"]
    #
    #     assert "attributes" in cmd_create_data
    #     assert "id" in cmd_create_data
    #     assert cmd_create_data["attributes"]["token"] == "paradigmshift3d"
    #     assert cmd_create_data["attributes"]["enabled"] is True
    #     assert cmd_create_data["attributes"]["name"] == name
    #     assert cmd_create_data["type"] == "command"
    #
    #     # The submitted data does not have these keys and we already asserted
    #     # them, so add them so the final test can complete
    #     self.creation_data[1]["token"] = self.data["attributes"]["token"]
    #     self.creation_data[1]["enabled"] = self.data["attributes"]["enabled"]
    #
    #     assert cmd_create_data["attributes"] == self.creation_data[1]
    #
    #     cmd = client.get(self.url)
    #     cmd_all_data = cmd.json["data"]
    #     assert len(cmd_all_data) == 2
    #
    #     for result in cmd_all_data:
    #         found = False
    #         name = result["attributes"]["name"]
    #         for value in self.creation_data:
    #             if value["name"] == name:
    #                 assert result["attributes"] == value
    #                 found = True
    #         # Check if the command was found in the creation data
    #         if not found:
    #             raise AssertionError("Command not found")
    #
    # def test_edit(self, client):
    #     edit_data = {
    #         "enabled": False,
    #         "response": {
    #             "message": [
    #                 {
    #                     "type": "emoji",
    #                     "data": "smile",
    #                     "text": ":)"
    #                 }
    #             ]
    #         }
    #     }
    #     edit_name = self.creation_data[0]["name"]
    #
    #     cmd = client.patch(
    #         self.url + "/" + edit_name,
    #         data=dumps(edit_data),
    #         content_type="application/json"
    #     )
    #
    #     cmd_edit_data = cmd.json
    #
    #     assert cmd_edit_data["meta"]["edited"] is True
    #     assert cmd_edit_data["data"]["attributes"]["enabled"] is False
    #     assert cmd_edit_data["data"]["attributes"][
    #         "response"]["message"] == edit_data["response"]["message"]
    #
    # def test_removal(self, client):
    #     """Remove a command and see if it matches"""
    #     # Using the quote ID from the first created quote
    #     cmd = client.delete(
    #         self.url + "/" + str(self.data["attributes"]["name"]))
    #     deletion_data = cmd.json
    #
    #     assert deletion_data["meta"]["deleted"][
    #         "command"][0] == self.data["id"]
