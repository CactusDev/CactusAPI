"""Tests the repeat endpoint of the API"""
import json


class TestRepeats:
    """Tests the repeat endpoint of the API"""
    creation_data = {}
    url = "/api/v1/user/paradigmshift3d/repeat"

    def test_create(self, client, api_auth):
        """Valid repeat creation"""
        # Create repeat
        # Check that repeat has correct period and command name
        # Check repeat's type | assert data["type"] == "repeat"
        pass

    def test_single(self, client, api_auth):
        """A test that does stuff, namely checking if stuff == other stuff"""
        # Create repeat
        # Retrieve repeat
        # Check that repeat has correct period and command name
        # Make sure created ID is same as retrieved ID
        # Delete repeat
        pass

    def test_all(self, client, api_auth):
        # Retrieve all repeat objects
        # Make sure that the proper repeat objects have been returned
        # Delete all repeat objects
        pass

    def test_delete(self, client, api_auth):
        """Test to see if the services are being removed properly"""
        # Create repeat
        # Get created repeat's ID
        # Delete repeat by same name
        # Make sure deleted 's ID is same as created's
        # assert created_id == deleted_data["id"]
        pass
