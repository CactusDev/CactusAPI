import pytest
import json


class TestQuotes:
    creation_data = [{"quote": "Cacti rock!"}, {"quote": "CactusBot!"}]
    url = "/api/v1/user/paradigmshift3d/quote"

    def test_create(self, client, api_auth):
        """Valid quote creation"""
        quote = client.post(
            self.url, data=self.creation_data[0], headers=api_auth)

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

    def test_single(self, client, api_auth):
        """Create a single quote object and see if it matches"""
        quote = client.post(
            self.url, data=self.creation_data[1], headers=api_auth)

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

        assert quote_single_data["data"]["attributes"]["quoteId"] == 2
        assert quote_single_data["data"]["attributes"][
            "quote"] == self.creation_data[1]["quote"]
        assert quote_single_data["data"]["id"] == data["data"]["id"]

    def test_all(self, client, api_auth):
        """Retrieve all quotes"""
        for to_create in self.creation_data:
            index = self.creation_data.index(to_create)
            quote = client.post(
                self.url, data=to_create, headers=api_auth)
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
        quote = client.get(self.url, data={"random": "true"})
        if hasattr(quote, "json"):
            quote = quote.json
        else:
            quote = json.loads(quote.data.decode('utf-8'))

        i = 0
        while i < 10:
            quote_internal = client.get(
                self.url, data={"random": "true", "limit": 1}).json
            if quote_internal["data"][0]["attributes"] != quote["data"][0]["attributes"]:
                # It's a different quote, thus ?random=true is working
                break

            i += 1

        if i == 10:
            raise AssertionError(
                "No random results returned within attempt limit")
    #

    def test_removal(self, client, api_auth):
        """Remove a quote and see if it matches"""
        quote_create = client.post(
            self.url, data=self.creation_data[0], headers=api_auth)
        creation_data = quote_create.json

        quote_id = creation_data["data"]["attributes"]["quoteId"]

        quote = client.delete(self.url + '/' + str(quote_id), headers=api_auth)
        deletion_data = quote.json

        assert deletion_data["meta"]["deleted"][
            0] == creation_data["data"]["id"]
