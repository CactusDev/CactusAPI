"""Tests the trust endpoint of the API"""
import json
import pytest


class TestTrusts:
    """Tests the trust endpoint of the API"""
    creation_data = {
        "ParadigmShift3d": "24228",
        "CactusBotDev": "25873"
    }
    url = "/api/v1/user/paradigmshift3d/trust"

    def test_create(self, client, api_auth):
        """Valid trust creation"""
        name = "ParadigmShift3d"
        trust = client.patch(self.url + '/' + self.creation_data[name],
                             data=json.dumps({"userName": name}),
                             content_type="application/json",
                             headers=api_auth)
        data = json.loads(trust.data.decode())
        assert data["meta"].get("created", False)
        data = data["data"]
        assert data["type"] == "trust"

        assert data["attributes"]["token"] == "paradigmshift3d"
        assert data["attributes"]["userName"] == name
        assert data["attributes"]["userId"] == self.creation_data[name]

    def test_single(self, client, api_auth):
        """A test that does stuff, namely checking if stuff == other stuff"""
        name = "CactusBotDev"
        trust = client.patch(self.url + '/' + self.creation_data[name],
                             data=json.dumps({"userName": name}),
                             content_type="application/json",
                             headers=api_auth)
        created_id = json.loads(trust.data.decode()).get("data", {}).get("id")
        assert created_id is not None

        trust = client.get(self.url + '/' + self.creation_data[name])
        data = json.loads(trust.data.decode())["data"]
        assert data["type"] == "trust"

        assert data["attributes"]["token"] == "paradigmshift3d"
        assert data["attributes"]["userName"] == name
        assert data["attributes"]["userId"] == self.creation_data[name]

        assert data["id"] == created_id

    def test_all(self, client, api_auth):
        trust = client.get(self.url)
        data = json.loads(trust.data.decode())

        for trust in data["data"]:
            # Should be the same for all returned
            assert trust["attributes"]["token"] == "paradigmshift3d"
            assert trust["type"] == "trust"
            deleted = client.delete(
                self.url + '/' + trust["attributes"]["userId"],
                headers=api_auth
            )

            # Assert the trust resource was deleted properly
            assert deleted.status_code == 200

        test_userid = set(trust["attributes"]["userId"]
                          for trust in data["data"])
        test_username = set(trust["attributes"]["userName"]
                            for trust in data["data"])

        assert test_userid == set(self.creation_data.values())
        assert test_username == set(self.creation_data.keys())

    def test_delete(self, client, api_auth):
        """Test to see if the services are being removed properly"""
        name = "CactusBotDev"
        trust = client.patch(self.url + '/' + self.creation_data[name],
                             data=json.dumps({"userName": name}),
                             content_type="application/json",
                             headers=api_auth)
        created_id = json.loads(trust.data.decode()).get("data", {}).get("id")
        assert created_id is not None

        deleted = client.delete(self.url + '/' + self.creation_data[name],
                                headers=api_auth)
        data = json.loads(deleted.data.decode())

        assert len(data["meta"]["deleted"]) == 1
        assert data["meta"]["deleted"][0] == created_id
