import json
import sys
import os, binascii
import getpass

class Bank:
    def __init__(self):
        self.account_dir = 'accounts/'
        if not os.path.exists(self.account_dir):
            os.makedirs(self.account_dir)
        self.select_operation()

    def select_operation(self):
        print "Please choose a number (1 - 5) to select one of the operation below:"
        print "  ( 1 ) Open a bank account"
        print "  ( 2 ) Close your bank account"
        print "  ( 3 ) Withdraw from your bank account"
        print "  ( 4 ) Deposit into a bank account"
        print "  ( 5 ) Exit"
        self.operation = raw_input()
        while self.operation != "5":
            self.start_operation()

    def start_operation(self):
        if self.operation == '1':
            self.open_account()
        elif self.operation == '2':
            self.close_account()
        elif self.operation == '3':
            self.withdraw()
        elif self.operation == '4':
            self.deposit()
        elif self.operation == '5':
            sys.exit()
        else:
            print "We don't recognize this operation. Please enter an integer from 1 to 5."
            self.select_operation()

    def open_account(self):
        self.username = raw_input("Please enter your full name: ")
        print "Please enter a password (length must be at least 4)"
        self.password  = getpass.getpass()
        while len(self.password) < 4:
            print "Please enter a password (length must be at least 4)"
            self.password  = getpass.getpass()
        self.account_id = binascii.b2a_hex(os.urandom(4))
        if self.existed() is False:
            self.save_account()
        else:
            print "This account already exists."
            print "Please choose another operation."
            self.select_operation()

    def close_account(self):
        self.check_indentity()
        old_filename = self.account_dir + self.account_id + '.json'
        new_filename = self.account_dir + '[closed]' + self.account_id + '.json'
        os.rename(old_filename, new_filename)
        print "Your account is successfully closed"

    def deposit(self):
        self.account_id = raw_input("Please enter account id you want to deposit into: ").lower()
        if self.existed() == True:
            action = 'deposit'
            deposit_amt = input("How much do you want to deposit: $")
            while (isinstance(deposit_amt, int) == False) and (isinstance(deposit_amt, float) == False) and (deposit_amt < 0):
                deposit_amt = float(raw_input("How much do you want to deposit: $"))
                print "You must enter a positve number. Please try again"
            print "You have deposited $%d" % deposit_amt
            self.update_data(action, deposit_amt)
        else:
            print "Account id does not exist. Please retry."
            self.deposit()

    def withdraw(self):
        self.check_indentity()
        withdraw_amt = input("How much do you want to withdraw: $")
        filename = self.account_dir + self. account_id + ".json"
        jsonFile = open(filename, 'r')
        data = json.load(jsonFile)
        while withdraw_amt > data['balance'] or withdraw_amt < 0:
            print "Your withdrawal exceeded your account balance. Your balance is currently $%d. Please try again." % data['balance']
            withdraw_amt = input("How much do you want to withdraw: $")
        action = 'withdraw'
        print "You have withdrawed $%d" % withdraw_amt
        self.update_data(action, withdraw_amt)

    def save_account(self):
        data = { 'username': self.username,
                 'password': self.password,
                 'account_id': self.account_id,
                 'balance': 0
               }
        filename = self.account_dir + self.account_id + ".json"
        with open(filename, 'w') as outfile:
            json.dump(data, outfile)
        print "Your acount is successfully created."
        print "Your account id is " + self.account_id

    def update_data(self, action, amt):
        filename = self.account_dir + self. account_id + ".json"
        jsonFile = open(filename, 'r')
        data = json.load(jsonFile)
        if action == 'withdraw':
            data["balance"] -= amt
        elif action == 'deposit':
            data["balance"] += amt
        with open(filename, 'w') as jsonFile:
            jsonFile.write(json.dumps(data))


    def check_indentity(self):
        self.account_id = raw_input("Please enter your account id: ").lower()
        print "Please enter your password: "
        self.password = getpass.getpass()

        if self.existed() == True and self.check_password() == True:
            return True
        else:
            print "You may enter wrong account id or password. Operation exited."

    def check_password(self):
        filename = self.account_dir + self.account_id + ".json"
        jsonFile = open(filename, 'r')
        data = json.load(jsonFile)
        if self.password == data['password']:
            return True
        else:
            return False

    def existed(self):
        current_filename = self.account_id + ".json"
        existed_account_files = os.listdir(self.account_dir)
        if current_filename in existed_account_files:
            return True
        else:
            return False

new_operation = Bank()
