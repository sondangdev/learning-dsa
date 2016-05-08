import json
import os

class Database:
    def __init__(self):
        self.database = 'accounts.json'
        if not os.path.isfile(self.database):
            with open(self.database, 'w+') as json_file:
                data = {}
                return json_file.write(json.dumps(data))

    def save(self, data):
        with open(self.database, 'w') as json_file:
            return json_file.write(json.dumps(data))

    def load(self):
        with open(self.database, 'r') as json_file:
            return json.load(json_file)
