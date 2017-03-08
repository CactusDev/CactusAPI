"""Tests the alias endpoint of the API"""
import json


class TestAliases:
    """Tests the social endpoint of the API"""
    creation_data = {}
    url = "/api/v1/user/paradigmshift3d/alias"

    def test_create(self, client, api_auth):
        """Valid social service creation"""
        # Create command to be aliased
        # Create alias
        # Check that alias is proper name & has proper args
        # Check that alias' command key == command created
        # Check alias' type | assert data["type"] == "alias"
        # Delete command
        # Check that alias is properly removed
        pass

    def test_single(self, client, api_auth):
        """A test that does stuff, namely checking if stuff == other stuff"""
        # Create command to be aliased
        # Retrieve alias
        # Check that alias' command key == command created
        # Check that alias is proper name & has proper args
        # Delete alias
        pass

    def test_delete(self, client, api_auth):
        """Test to see if the services are being removed properly"""
        # Create alias
        # Get created alias' ID
        # Delete alias by same name
        # Make sure deleted alias' ID is same as created's
        # assert created_id == deleted_data["id"]
        pass
