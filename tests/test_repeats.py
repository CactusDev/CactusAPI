"""Tests the repeat endpoint of the API"""
import json


class TestRepeats:
    """Tests the repeat endpoint of the API"""
    creation_data = {
        "test": {
            "period": 60000,
            "commandName": "foo"
        },
        "potato": {
            "period": 960000,
            "commandName": "foo"
        }
    }
    url = "/api/v1/user/paradigmshift3d/repeat"

    def test_create(self, client, api_auth, command_data):
        """Valid repeat creation"""
        name = "test"
        cmd_name = "foo"
        cmd = client.patch("/api/v1/user/paradigmshift3d/command/" + cmd_name,
                           data=json.dumps(command_data[cmd_name]),
                           content_type="application/json",
                           headers=api_auth)

        # The command was created successfully, so we can continue
        assert cmd.status_code == 201
        created_id = json.loads(cmd.data.decode())["data"]["id"]

        repeat = client.patch(self.url + '/' + name,
                              data=json.dumps(self.creation_data[name]),
                              content_type="application/json",
                              headers=api_auth)
        data = json.loads(repeat.data.decode())["data"]
        assert repeat.status_code == 201
        assert data["type"] == "repeat"

        assert data["attributes"]["repeatName"] == name
        assert data["attributes"]["token"] == "paradigmshift3d"
        assert data["attributes"]["command"]["id"] == created_id
        assert data["attributes"][
            "commandName"] == self.creation_data[name]["commandName"]
        assert data["attributes"][
            "period"] == self.creation_data[name]["period"]

    def test_single(self, client, api_auth):
        """A test that does stuff, namely checking if stuff == other stuff"""
        name = "potato"

        repeat = client.patch(self.url + '/' + name,
                              data=json.dumps(self.creation_data[name]),
                              content_type="application/json",
                              headers=api_auth)
        created_id = json.loads(repeat.data.decode())["data"]["id"]
        assert repeat.status_code == 201

        repeat = client.get(self.url + '/' + name)
        data = json.loads(repeat.data.decode())["data"]
        assert data["attributes"]["repeatName"] == name
        assert data["attributes"]["token"] == "paradigmshift3d"
        assert data["attributes"]["command"]["id"] == created_id
        assert data["attributes"][
            "commandName"] == self.creation_data[name]["commandName"]
        assert data["attributes"][
            "period"] == self.creation_data[name]["period"]

    def test_all(self, client, api_auth):
        # Retrieve all repeat objects
        # Make sure that the proper repeat objects have been returned
        # Delete all repeat objects
        pass

    def test_delete(self, client, api_auth):
        """Test to see if the services are being removed properly"""
        # Create repeat
        # Get created repeat's ID
        # Delete repeat by same name
        # Make sure deleted 's ID is same as created's
        # assert created_id == deleted_data["id"]
        pass
