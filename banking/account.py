import json
import datetime
import os
import binascii
from database import Database

class Account:
    def __init__(self):
        self.database = Database()
        self.records = self.database.load()

    def update(self, account_id, amt):
        if amt < 0:
            self.records[account_id]['history'][self.timestamp()] = str(amt)
        elif amt > 0:
            self.records[account_id]['history'][self.timestamp()] = '+' + str(amt)
        self.records[account_id]['balance'] += amt
        self.database.save(self.records)

    def delete(self, account_id):
        del self.records[account_id]
        self.database.save(self.records)

    def create(self, username, password):
        account_id = self.generate_id()
        while (account_id in self.records.keys()):
            account_id = self.generate_id()
        self.records[account_id] = {
                'username': username,
                'password': password,
                'balance': 0,
                'history': { self.timestamp(): '0' }
        }
        self.database.save(self.records)
        return account_id

    def generate_id(self):
        return binascii.b2a_hex(os.urandom(4))

    def timestamp(self):
        return str(datetime.datetime.now())
