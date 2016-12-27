import pytest


class TestQuotes:
    creation_data = [{"quote": "Cacti rock!"}, {"quote": "CactusBot!"}]
    url = "/api/v1/user/paradigmshift3d/quote"
    data = {}

    def test_create(self, client):
        """Valid quote creation"""
        quote = client.post(self.url, data=self.creation_data[0])
        self.data.update(quote.json)

        assert "attributes" in self.data["data"]
        assert "id" in self.data["data"]
        assert self.data["data"]["attributes"]["quoteId"] == 1
        assert self.data["data"]["attributes"][
            "quote"] == self.creation_data[0]["quote"]

    def test_single(self, client):
        """Get a single quote object and see if it matches (it should)"""
        quote = client.get(
            self.url + "/" + str(self.data["data"]["attributes"]["quoteId"]))
        quote_single_data = quote.json

        assert quote_single_data["data"]["attributes"]["quoteId"] == 1
        assert quote_single_data["data"]["attributes"][
            "quote"] == self.creation_data[0]["quote"]
        assert quote_single_data["data"]["id"] == self.data["data"]["id"]

    def test_all(self, client):
        """Retrieve all quotes"""
        # Create the second quote
        quote = client.post(self.url, data=self.creation_data[1])
        quote_create_data = quote.json

        assert quote_create_data["data"]["attributes"]["quoteId"] == 2
        assert quote_create_data["data"]["attributes"][
            "quote"] == self.creation_data[1]["quote"]

        quote = client.get(self.url)
        quote_all_data = quote.json
        assert len(quote_all_data["data"]) == 2

    def test_random(self, client):
        # API should return random result within 5 requests normally
        quote = client.get(
            self.url + "/" + str(self.data["data"]["attributes"]["quoteId"]),
            data={"random": "true"}
        ).json

        i = 0
        while i < 5:
            quote_internal = client.get(
                self.url, data={"random": "true", "limit": 1}).json
            if quote_internal["data"][0]["attributes"] != quote["data"]["attributes"]:
                # It's a different quote, thus ?random=true is working
                break

            i += 1

        if i == 5:
            raise AssertionError(
                "No random results returned within attempt limit")

    def test_removal(self, client):
        """Remove a user and see if it matches"""
        # Using the quote ID from the first created quote
        quote = client.delete(
            self.url + "/" + str(self.data["data"]["attributes"]["quoteId"]))
        deletion_data = quote.json

        assert deletion_data["meta"]["deleted"][0] == self.data["data"]["id"]
