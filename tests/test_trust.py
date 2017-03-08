"""Tests the trust endpoint of the API"""
import json


class TestTrusts:
    """Tests the trust endpoint of the API"""
    creation_data = {}
    url = "/api/v1/user/paradigmshift3d/trust"

    def test_create(self, client, api_auth):
        """Valid trust creation"""
        # Create trust
        # Check that trust is proper userName & userId
        # Check trust's type | assert data["type"] == "alias"
        pass

    def test_single(self, client, api_auth):
        """A test that does stuff, namely checking if stuff == other stuff"""
        # Create trust to be aliased
        # Retrieve trust
        # Check that trust is proper userName & userId
        # Make sure created ID is same as retrieved ID
        # Delete trust
        pass

    def test_all(self, client, api_auth):
        # Retrieve all trust objects
        # Make sure that the proper trust objects have been returned
        # Delete all trust objects
        pass

    def test_delete(self, client, api_auth):
        """Test to see if the services are being removed properly"""
        # Create trust
        # Get created trust's ID
        # Delete trust by same name
        # Make sure deleted trust's ID is same as created's
        # assert created_id == deleted_data["id"]
        pass
