import pytest
import json


class TestQuotes:
    creation_data = [{"quote": "Cacti rock!"}, {"quote": "CactusBot!"}]
    url = "/api/v1/user/paradigmshift3d/quote"

    def test_create(self, client):
        """Valid quote creation"""
        quote = client.post(self.url, data=self.creation_data[0])

        if hasattr(quote, "json"):
            update_data = quote.json
        else:
            update_data = json.loads(quote.data.decode('utf-8'))

        assert "data" in update_data
        assert "attributes" in update_data["data"]
        assert "id" in update_data["data"]
        assert update_data["data"]["attributes"]["quoteId"] == 1
        assert update_data["data"]["attributes"][
            "quote"] == self.creation_data[0]["quote"]

    def test_single(self, client):
        """Get a single quote object and see if it matches (it should)"""

        quote = client.post(self.url, data=self.creation_data[0])

        if hasattr(quote, "json"):
            data = quote.json
        else:
            data = json.loads(quote.data.decode('utf-8'))

        quote = client.get(
            self.url + "/" + str(data["data"]["attributes"]["quoteId"]))

        if hasattr(quote, "json"):
            quote_single_data = quote.json
        else:
            quote_single_data = json.loads(quote.data.decode('utf-8'))

        assert quote_single_data["data"]["attributes"]["quoteId"] == 1
        assert quote_single_data["data"]["attributes"][
            "quote"] == self.creation_data[0]["quote"]
        assert quote_single_data["data"]["id"] == data["data"]["id"]

    def test_all(self, client):
        """Retrieve all quotes"""
        for to_create in self.creation_data:
            index = self.creation_data.index(to_create)
            quote = client.post(self.url, data=to_create)
            if hasattr(quote, "json"):
                quote_create_data = quote.json
            else:
                quote_create_data = json.loads(quote.data.decode('utf-8'))

            assert quote_create_data["data"][
                "attributes"]["quoteId"] == index + 1
            assert quote_create_data["data"]["attributes"][
                "quote"] == self.creation_data[index]["quote"]

        quote = client.get(self.url)
        if hasattr(quote, "json"):
            quote_all_data = quote.json
        else:
            quote_all_data = json.loads(quote.data.decode('utf-8'))
        assert len(quote_all_data["data"]) == 2

    def test_random(self, client):
        # API should return random result within 5 requests normally
        quote = client.get(
            self.url + "/" + str(self.data["data"]["attributes"]["quoteId"]),
            data={"random": "true"}
        )
        if hasattr(quote, "json"):
            quote = quote.json
        else:
            quote = json.loads(quote.data.decode('utf-8'))

        i = 0
        while i < 10:
            quote_internal = client.get(
                self.url, data={"random": "true", "limit": 1}).json
            if quote_internal["data"][0]["attributes"] != quote["data"]["attributes"]:
                # It's a different quote, thus ?random=true is working
                break

            i += 1

        if i == 10:
            raise AssertionError(
                "No random results returned within attempt limit")
    #
    # def test_removal(self, client):
    #     """Remove a user and see if it matches"""
    #     # Using the quote ID from the first created quote
    #     quote = client.delete(
    #         self.url + "/" + str(self.data["data"]["attributes"]["quoteId"]))
    #     deletion_data = quote.json
    #
    #     assert deletion_data["meta"]["deleted"][0] == self.data["data"]["id"]
