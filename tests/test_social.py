"""Tests the social endpoint of the API"""
import json


class TestSocial:
    """Tests the social endpoint of the API"""
    creation_data = {
        "github": {"url": "https://github.com/CactusDev"},
        "twitter": {"url": "https://twitter.com/CactusDevTeam"}
    }
    url = "/api/v1/user/paradigmshift3d/social"

    def test_create(self, client, api_auth):
        """Valid social service creation"""
        service = "github"
        social = client.patch(
            self.url + '/' + service,
            data=self.creation_data[service],
            headers=api_auth
        )

        data = json.loads(social.data.decode())
        assert data["meta"]["created"] is True

        data = data["data"]
        assert data["type"] == "social"
        assert data["attributes"]["service"] == service.lower()
        assert data["attributes"]["url"] == self.creation_data[service]["url"]

    def test_single(self, client, api_auth):
        """A test that does stuff, namely checking if stuff == other stuff"""
        service = "twitter"
        social = client.patch(
            self.url + '/' + service,
            data=self.creation_data[service],
            headers=api_auth
        )

        data = json.loads(social.data.decode())["data"]

        assert data["attributes"]["service"] == service.lower()
        assert data["attributes"]["url"] == self.creation_data[service]["url"]
        creation_id = data["id"]

        single = client.get(self.url + '/' + service)
        data = json.loads(single.data.decode())["data"]

        assert data["id"] == creation_id

    def test_all(self, client, api_auth):
        """
        Another test that does stuff, this time checking to see if lots of
        stuff == other lots of stuff
        """
        social_all = client.get(self.url)

        data = json.loads(social_all.data.decode())["data"]

        assert len(data) == 2
        assert set(serv["attributes"]["service"] for serv in data) == set(
            service.lower() for service in self.creation_data.keys())

        for service in data:
            cur_service = service["attributes"]["service"]
            cur_service_url = service["attributes"]["url"]
            assert cur_service_url == self.creation_data[cur_service]["url"]
            client.delete(self.url + '/' + cur_service, headers=api_auth)

    def test_delete(self, client, api_auth):
        """Test to see if the services are being removed properly"""
        service = "twitter"
        social = client.patch(
            self.url + '/' + service,
            data=self.creation_data[service],
            headers=api_auth
        )
        creation_id = json.loads(social.data.decode())["data"]["id"]

        deleted = client.delete(
            self.url + '/' + service,
            headers=api_auth
        )
        deleted_data = json.loads(deleted.data.decode())

        assert len(deleted_data["meta"]["deleted"]) == 1
        assert deleted_data["meta"]["deleted"][0] == creation_id
