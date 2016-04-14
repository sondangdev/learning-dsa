import json
import sys
import getpass
from account import Account
from authorization import Authorization

class Operation:
    def __init__(self):
        self.authorized = False
        self.start()

    def start(self):
        self.login_prompt()
        response = raw_input()
        self.login(response)

    def login_prompt(self):
        print "Please choose a number (1 - 3) to select one of the operation below:"
        print "  ( 1 ) Open a bank account"
        print "  ( 2 ) Deposit to a bank account"
        print "  ( 3 ) Login to your bank account"
        print "  ( 4 ) Exit"

    def login(self, response):
        if response == '1':
            self.open_account()
        elif response == '2':
            self.deposit()
        elif response == '3':
            self.authorize()
            self.select_operation()
        elif response == '4':
            print "Thank you for using our service."
            sys.exit()
        else:
            print "We don't recognize this operation."
            print "Please enter an integer in range 1 to 4."
            self.start()

    def authorize(self):
        self.account_id = raw_input("Please enter your account id: ").lower()
        self.password = getpass.getpass()
        authorization = Authorization(self.account_id, self.password)
        while authorization.check_identity() == False:
            print "You may enter wrong account id or password. Please try again."
            self.allow_cancel()
            self.authorize()
        self.authorized = True

    def operation_prompt(self):
        print "Please choose a number (1 - 4) to select one of the operation below:"
        print "  ( 1 ) Close your bank account"
        print "  ( 2 ) Withdraw from your bank account"
        print "  ( 3 ) Deposit into another bank account"
        print "  ( 4 ) Exit"

    def select_operation(self):
        self.operation_prompt()
        response = raw_input()
        self.start_operation(response)

    def start_operation(self, response):
        if response == '1':
            self.close_account()
        elif response == '2':
            self.withdraw()
        elif response == '3':
            self.deposit()
        elif response == '4':
            print "Thank you for using our service."
            sys.exit()
        else:
            print "We don't recognize this operation."
            print "Please enter an integer in range 1 to 4."
            self.select_operation()

    def open_account(self):
        username = raw_input("Please enter your full name: ")
        password  = ""
        while len(password) < 4:
            print "Please enter a password  with length of at least 4"
            password  = getpass.getpass()
        self.account_id = Account().create(username, password)
        print "Your acount is successfully created."
        print "Your account id is " + self.account_id
        self.authorized = True
        self.select_operation()

    def close_account(self):
        self.is_authorized()
        print "WARNING: This action is irreversible."
        res = raw_input("Are you sure you want to close this account? (y/n): ").lower()
        if res == "y":
            Account().delete(self.account_id)
            print "Your account is successfully closed"
            self.authorized = False
            self.start()
        else:
            self.select_operation()

    def is_authorized(self):
        if self.authorized == False:
            self.authorize()

    def deposit(self):
        account_id = raw_input("Please enter account id you want to deposit into: ").lower()
        authorization = Authorization(account_id, "")
        if authorization.check_account_id() == True:
            amt = input("How much do you want to deposit: $")
            while (
                isinstance(amt, int) == False
                and isinstance(amt, float) == False
                and (amt < 0)
                ):
                amt = float(raw_input("How much do you want to deposit: $"))
                print "You must enter a positive number. Please try again"
                self.allow_cancel()
            print "You have deposited $%d" % amt
            Account().update(account_id, amt)
            if self.authorized == True:
                self.select_operation()
            else:
                self.start()

        else:
            print "Account id does not exist. Please retry."
            self.allow_cancel()
            self.deposit()

    def withdraw(self):
        self.is_authorized()
        amt = input("How much do you want to withdraw: $")
        data = Account().records[self.account_id]
        while amt > data['balance'] or amt < 0:
            print "Your withdrawal exceeded your account balance. Your balance is currently $%d. Please try again." % data['balance']
            self.allow_cancel()
            amt = input("How much do you want to withdraw: $")
        print "You have withdrawed $%d" % amt
        amt = -amt
        Account().update(self.account_id, amt)
        self.select_operation()

    def allow_cancel(self):
        print("Do you want to continue (y/n):" )
        response = raw_input().lower()
        if response == 'n':
            if self.authorized == True:
                self.select_operation()
            else:
                self.start()
