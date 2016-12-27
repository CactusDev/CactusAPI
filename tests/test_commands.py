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
        name = self.creation_data[0].pop("name")
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
        self.creation_data[name]["token"] = self.data["attributes"]["token"]
        self.creation_data[name]["enabled"] = self.data[
            "attributes"]["enabled"]
        self.creation_data[name]["name"] = self.data["attributes"]["name"]

        assert self.data["attributes"] == self.creation_data[0]

    def test_single(self, client):
        """Get a single user object and see if it matches (it should)"""
        cmd = client.get(self.url + "/" + str(self.data["attributes"]["name"]))
        cmd_single_data = cmd.json["data"]

        assert cmd_single_data["attributes"] == self.data["attributes"]
        assert cmd_single_data["id"] == self.data["id"]

    def test_all(self, client):
        # Create the second command
        quote = client.post(self.url, data=self.creation_data[1])
        quote_create_data = quote.json

        assert quote_create_data["data"]["attributes"]["quoteId"] == 2
        assert quote_create_data["data"]["attributes"][
            "quote"] == self.creation_data[1]["quote"]

        quote = client.get(self.url)
        quote_all_data = quote.json
        assert len(quote_all_data["data"]) == 2
    #
    #
    # def test_edit(self, client):
    #     pass
    #
    # def test_removal(self, client):
    #     """Remove a user and see if it matches"""
    #     # Using the quote ID from the first created quote
    #     quote = client.delete(
    #         self.url + "/" + str(self.data["data"]["attributes"]["quoteId"]))
    #     deletion_data = quote.json
    #
    #     assert deletion_data["meta"]["deleted"][0] == self.data["data"]["id"]
