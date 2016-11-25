import app
import unittest
import pickle
import json


class APITestCase(unittest.TestCase):

    def setUp(self):
        app.app.config["TESTING"] = True
        app.app.config["RDB_DB"] = "unittests"
        self.app = app.app.test_client()
        self.root = "/api/v1"
        self.token = "testuser"
        with open("unittests/data.pickle", 'rb') as f:
            self.compare = pickle.load(f)

    def test_get_single_command(self):
        cmd = self.app.get("{root}/user/{token}/command/spam".format(
            root=self.root,
            token=self.token
        ))
        json_data = json.loads(cmd.get_data().decode())
        self.maxDiff = None
        self.assertDictEqual(json_data, self.compare["command_single"])

if __name__ == "__main__":
    unittest.main()
