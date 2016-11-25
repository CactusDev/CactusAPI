import pickle

data = {
    "command_single": {
        "data": {
            "attributes": {
                "createdAt": "Fri Nov 25 15:14:40 2016",
                "name": "spam",
                "response": {
                    "action": False,
                    "message": [
                        {
                            "data": "lol! ",
                            "text": "lol! ",
                            "type": "text"
                        },
                        {
                            "data": "🌵",
                            "text": ":cactus",
                            "type": "emoji"
                        }
                    ],
                    "role": 0,
                    "target": None,
                    "user": ""
                },
                "token": "testuser",
                "userLevel": 0
            },
            "id": "2989918d-5b98-4ed3-a3b9-dbf2449f7844",
            "type": "command"
        }
    },
    "command_many": {
        "data": [
            {
                "attributes": {
                    "createdAt": "Fri Nov 25 15:21:09 2016",
                    "name": "raided",
                    "response": {
                        "action": False,
                        "message": [
                            {
                                "data": "Whoa! Thanks raiders!",
                                "text": "lol! ",
                                "type": "text"
                            }
                        ],
                        "role": 0,
                        "target": None,
                        "user": ""
                    },
                    "token": "testuser",
                    "userLevel": 0
                },
                "id": "5099408b-916e-4f31-b864-98afeea6e3e2",
                "type": "command"
            },
            {
                "attributes": {
                    "createdAt": "Fri Nov 25 15:21:09 2016",
                    "name": "spam",
                    "response": {
                        "action": False,
                        "message": [
                            {
                                "data": "spam eggs",
                                "text": "spam eggs ",
                                "type": "text"
                            }
                        ],
                        "role": 0,
                        "target": None,
                        "user": ""
                    },
                    "token": "testuser",
                    "userLevel": 0
                },
                "id": "4787acaf-9cae-4240-b074-f26ae87f0e83",
                "type": "command"
            },
            {
                "attributes": {
                    "createdAt": "Fri Nov 25 15:21:09 2016",
                    "name": "foo",
                    "response": {
                        "action": False,
                        "message": [
                            {
                                "data": "bar!",
                                "text": "bar! ",
                                "type": "text"
                            }
                        ],
                        "role": 0,
                        "target": None,
                        "user": ""
                    },
                    "token": "testuser",
                    "userLevel": 0
                },
                "id": "c7ac3ab7-136f-4520-88e9-a26f34226f87",
                "type": "command"
            }
        ]
    }}

with open("data.pickle", 'wb') as f:
    pickle.dump(data, f)
