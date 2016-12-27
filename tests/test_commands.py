import pytest
from json import dumps


class TestQuotes:
    creation_data = [
        {
            "name": "foo",
            "userLevel": 0,
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
            "userLevel": 0,
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

    def test_create(self, client):
        """Valid command creation"""
        # Get data from the creation_data dict
        name = self.creation_data[0]["name"]
        cmd = client.patch(self.url + "/" + name,
                           data=dumps(self.creation_data[0]),
                           content_type="application/json"
                           )
        self.data.update(cmd.json["data"])

        assert "attributes" in self.data
        assert "id" in self.data
        assert self.data["attributes"]["token"] == "paradigmshift3d"
        assert self.data["attributes"]["enabled"] == True
        assert self.data["attributes"]["name"] == name
        assert self.data["type"] == "command"

        # The submitted data does not have these keys and we already asserted
        # them, so add them so the final test can complete
        self.creation_data[0]["token"] = self.data["attributes"]["token"]
        self.creation_data[0]["enabled"] = self.data["attributes"]["enabled"]

        assert self.data["attributes"] == self.creation_data[0]

    def test_single(self, client):
        """Get a single user object and see if it matches (it should)"""
        cmd = client.get(self.url + "/" + self.data["attributes"]["name"])
        cmd_single_data = cmd.json["data"]

        assert cmd_single_data["attributes"] == self.data["attributes"]
        assert cmd_single_data["id"] == self.data["id"]

    def test_all(self, client):
        # Create the second command
        name = self.creation_data[1]["name"]
        print(name)
        quote = client.patch(
            self.url + "/" + name,
            data=dumps(self.creation_data[1]),
            content_type="application/json"
        )
        cmd_create_data = quote.json["data"]

        assert "attributes" in cmd_create_data
        assert "id" in cmd_create_data
        assert cmd_create_data["attributes"]["token"] == "paradigmshift3d"
        assert cmd_create_data["attributes"]["enabled"] == True
        assert cmd_create_data["attributes"]["name"] == name
        assert cmd_create_data["type"] == "command"

        # The submitted data does not have these keys and we already asserted
        # them, so add them so the final test can complete
        self.creation_data[1]["token"] = self.data["attributes"]["token"]
        self.creation_data[1]["enabled"] = self.data["attributes"]["enabled"]

        assert cmd_create_data["attributes"] == self.creation_data[1]

        cmd = client.get(self.url)
        cmd_all_data = cmd.json["data"]
        assert len(cmd_all_data) == 2

    # def test_edit(self, client):
    #     pass
    #
    def test_removal(self, client):
        """Remove a command and see if it matches"""
        # Using the quote ID from the first created quote
        quote = client.delete(
            self.url + "/" + str(self.data["attributes"]["name"]))
        deletion_data = quote.json

        print(deletion_data)

        assert deletion_data["meta"]["deleted"][
            "command"][0] == self.data["id"]
