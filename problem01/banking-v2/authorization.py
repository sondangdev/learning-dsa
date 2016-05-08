from account import Account

class Authorization:
    def __init__(self, account_id, password):
        self.account_id = account_id
        self.password = password

    def check_identity(self):
        return self.check_account_id() and self.check_password()

    def check_account_id(self):
        if bool(Account().records) == True:
          return self.account_id in Account().records.keys()
        else:
          return False

    def check_password(self):
        if bool(Account().records) == True:
          return self.password == Account().records[self.account_id]['password']
        else:
          return False
