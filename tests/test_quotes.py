import json


class TestQuotes:
    creation_data = {
        "rock": {"quote": "Cacti rock!"},
        "cactusbot": {"quote": "CactusBot!"}
    }
    url = "/api/v1/user/paradigmshift3d/quote"

    def test_create(self, client, api_auth):
        """Valid quote creation"""
        name = "rock"
        quote = client.post(
            self.url, data=self.creation_data[name], headers=api_auth)
        data = json.loads(quote.data.decode('utf-8'))

        assert "data" in data
        assert "attributes" in data["data"]
        assert "id" in data["data"]
        assert data["data"]["attributes"]["quoteId"] == 1
        assert data["data"]["attributes"][
            "quote"] == self.creation_data[name]["quote"]

    def test_edit(self, client, api_auth):
        # TODO
        pass

    def test_single(self, client, api_auth):
        """Create a single quote object and see if it matches"""
        name = "cactusbot"
        quote = client.post(
            self.url, data=self.creation_data[name], headers=api_auth)
        data = json.loads(quote.data.decode('utf-8'))

        quote = client.get(
            self.url + "/" + str(data["data"]["attributes"]["quoteId"]))

        if hasattr(quote, "json"):
            quote_single_data = quote.json
        else:
            quote_single_data = json.loads(quote.data.decode('utf-8'))

        assert quote_single_data["data"]["attributes"]["quoteId"] == 2
        assert quote_single_data["data"]["attributes"][
            "quote"] == self.creation_data[name]["quote"]
        assert quote_single_data["data"]["id"] == data["data"]["id"]

    def test_all(self, client):
        """Retrieve all quotes"""
        quote = client.get(self.url)
        quote_all_data = json.loads(quote.data.decode())["data"]
        assert len(quote_all_data) == 2
        quotes = sorted(
            [
                {
                    "quote": quote["attributes"]["quote"],
                    "quoteId": quote["attributes"]["quoteId"]
                }
                for quote in quote_all_data
            ],
            key=lambda quote: int(quote["quoteId"])
        )
        comparison = [
            {"quote": "Cacti rock!", "quoteId": 1},
            {"quote": "CactusBot!", "quoteId": 2}
        ]
        assert quotes == comparison

    def test_random(self, client, api_auth):
        # API should return random result within 5 requests normally
        quote = client.get(self.url, data={"random": "true"})
        data = json.loads(quote.data.decode('utf-8'))

        i = 0
        while i < 10:
            quote_internal = client.get(
                self.url, data={"random": "true", "limit": 1})
            quote_internal = json.loads(quote_internal.data.decode('utf-8'))

            if quote_internal["data"][0]["attributes"] != data["data"][0]["attributes"]:
                # It's a different quote, thus ?random=true is working
                break

            i += 1

        if i == 10:
            raise AssertionError(
                "No random results returned within attempt limit")

        for i in (1, 2):
            deleted = client.delete(self.url + '/' + str(i), headers=api_auth)
            assert deleted.status_code == 200

    def test_removal(self, client, api_auth):
        """Remove a quote and see if it matches"""
        quote_create = client.post(
            self.url, data=self.creation_data["rock"], headers=api_auth)
        creation_data = json.loads(quote_create.data.decode('utf-8'))

        quote_id = creation_data["data"]["attributes"]["quoteId"]

        quote = client.delete(self.url + '/' + str(quote_id), headers=api_auth)
        deletion_data = json.loads(quote.data.decode('utf-8'))

        assert len(deletion_data["meta"]["deleted"]) == 1
        assert deletion_data["meta"]["deleted"][
            0] == creation_data["data"]["id"]
