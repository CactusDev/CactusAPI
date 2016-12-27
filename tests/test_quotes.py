import pytest


@pytest.mark.usefixtures("client")
class TestQuotes:
    creation_data = [{"quote": "Cacti rock!"}, {"quote": "CactusBot!"}]
    url = "/api/v1/user/paradigmshift3d/quote"
    data = {}

    def test_create(self, client):
        """Valid user creation"""
        user = client.post(self.url, data=self.creation_data[0])
        self.data.update(user.json)
        assert "attributes" in self.data["data"]
        assert "id" in self.data["data"]

    def test_single(self, client):
        """Get a single user object and see if it matches (it should)"""
        self.url += "/" + str(self.data["data"]["attributes"]["quoteId"])
        user = client.get(self.url)
        user_single_data = user.json
        assert "id" in user_single_data["data"]
        assert user_single_data["data"]["id"] == self.data["data"]["id"]

    def test_all(self, client):
        user = client.post(self.url, data=self.creation_data[1])
        print(user.json)
        user = client.get(self.url)
        user_all_data = user.json
        assert len(user_all_data[""]) >= 2

    def test_removal(self, client):
        """Remove a user and see if it matches"""
        self.url += "/" + str(self.data["data"]["attributes"]["quoteId"])
        user = client.delete(self.url)
        deletion_data = user.json

        assert deletion_data["meta"]["deleted"][0] == self.data["data"]["id"]
