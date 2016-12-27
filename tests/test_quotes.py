import pytest


# @pytest.mark.userfixtures("client")
# class TestQuotes:
#     creation_data = {"quote": "Cacti rock!"}
#     url = "/api/v1/user/ParadigmShift3d/quote"
#     data = {}
#
#     def test_create(self):
#         # Valid user creation
#         user = client.post(self.url, data=self.creation_data)
#         self.data = user.json
#         assert "data" in self.data
#         assert "attributes" in self.data["data"]
#         assert "id" in self.data["data"]
#
#     def test_single(self):
#         user = client.get(self.url)
#         user_single_data = user.json
#         assert "data" in user_single_data
#         assert "attributes" in user_single_data["data"]
#         assert "id" in user_single_data["data"]
#         assert user_single_data["data"]["id"] == self.data["data"]["id"]
#
#     def test_removal(self):
#         user = client.delete(self.url)
#         deletion_data = user.json
#         assert "meta" in deletion_data
#         assert "deleted" in deletion_data["meta"]
#         assert deletion_data["meta"]["deleted"][0] == self.data["data"]["id"]
