import csv
import os


class Account:
    """
    Represents the bank account
    Attributes:
        - account_name(str): the name of the account holder
        - account_balance (float): the current balance of the account
        - bank_statement_filename (str): filename for the csv
    """

    def __init__(self, name, balance=0.00):
        """
        initializes an Account object
        Arguments:
        - name (str): the name of the account holder
        - balance (float, optional): the initial balance of the account
        Returns:
            - None
        """
        self.account_name = name
        self.account_balance = balance
        self.bank_statement_filename = "User_Statements.csv"

        # Create a bank statement CSV file if it doesn't exist
        if not os.path.exists(self.bank_statement_filename):
            with open(self.bank_statement_filename, 'w', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(['Account', 'Transaction Type', 'Amount', 'Previous Balance', 'Updated Balance'])

    def deposit(self, amount):
        """
        Deposits the specified amount into the Main Account
        Arguments:
        - amount (float): amount to deposit
        Returns:
        - Bool: if True the deposit is successful, otherwise False
        """
        if amount > 0:
            prev_balance = self.account_balance
            self.account_balance += amount
            self._log_transaction("Main Account", "Deposit", amount, prev_balance)
            return True
        return False

    def withdraw(self, amount):
        """
        Withdrawals the specified amount from the Main Account
        Arguments:
        - amount (float): Amount to withdrawal
        Returns:
        - Bool: if True the withdrawal is successful, otherwise False
        """
        if 0 < amount <= self.account_balance:
            prev_balance = self.account_balance
            self.account_balance -= amount
            self._log_transaction("Main Account", "Withdrawal", amount, prev_balance)
            return True
        return False

    def get_balance(self):
        """
        Gets the current balance of the account
        Returns:
            - float: current account balance
        """
        return self.account_balance

    def get_name(self):
        """
        Gets the name of the account holder
        Returns:
        - str: account holder's name
        """
        return self.account_name

    def _log_transaction(self, account_type, transaction_type, amount, prev_balance):
        """
        keeps log of the transactions via bank statement csv file
        Arguments:
        - account_type (str): type of account
        - transaction_type: type of transaction
        - amount (float): transaction amount
        - prev_balance (float): the previous balance of the account
        """
        with open(self.bank_statement_filename, 'a', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow([account_type, transaction_type, amount, prev_balance, self.account_balance])

        print(f"Transaction recorded for {account_type}: {transaction_type} of ${amount:.2f}")

    def get_total_balance(self):
        """
        calculates the total balance for the difference account type:
        Returns:
        - tuple: total balance for the Main and Savings Account
        """
        with open(self.bank_statement_filename, 'r') as csvfile:
            csv_reader = csv.reader(csvfile)
            main_account_total = 0
            savings_account_total = 0
            for row in csv_reader:
                if row[0] == 'Main Account':
                    if row[1] == 'Deposit':
                        main_account_total += float(row[2])
                    elif row[1] == 'Withdrawal':
                        main_account_total -= float(row[2])
                elif row[0] == 'Savings Account':
                    if row[1] == 'Deposit':
                        savings_account_total += float(row[2])
                    elif row[1] == 'Withdrawal':
                        savings_account_total -= float(row[2])
            return main_account_total, savings_account_total


class SavingAccount(Account):
    """
    Represents the savings account
    Attributes:
        - RATE (float): the interest rate
    """
    RATE = 0.02

    def __init__(self, name):
        """
        the initial amount within the SavingAccount
        Arguments:
        - name (str): Name of the account holder
        """
        super().__init__(name, 100.00)

    def deposit(self, amount):
        """
        Deposits the specific amount into the Savings Account
        Arguments:
        - amount (float): amount to deposit
        Returns:
        - Bool: if True the deposit is successful, otherwise False
        """
        if amount > 0:
            prev_balance = self.account_balance
            self.account_balance += amount
            self.apply_interest()  # Apply interest when depositing
            self._log_transaction("Savings Account", "Deposit", amount, prev_balance)
            return True
        return False

    def withdraw(self, amount):
        """
        Withdraws the specific amount from the Savings Account
        Arguments:
        - amount (float): Amount to withdrawal
        Returns:
        - Bool: if True the withdrawal is successful, otherwise False
        :param amount:
        :return:
        """
        if 0 < amount <= self.account_balance:
            prev_balance = self.account_balance
            self.account_balance -= amount
            self._log_transaction("Savings Account", "Withdrawal", amount, prev_balance)
            return True
        return False

    def apply_interest(self):
        """Applies the interest to the deposited amount"""
        interest = self.account_balance * self.RATE
        self.account_balance += interest

    def _log_transaction(self, account_type, transaction_type, amount, prev_balance):
        """
       sends transaction logs to the bank statement csv file
       Arguments:
       - account_type (str): type of account
       - transaction_type (str): type of transaction
       - amount (float): transaction amount
       - prev_balance (float): previous balance
       Returns:
           - None
       """
        with open(self.bank_statement_filename, 'a', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow([account_type, transaction_type, amount, prev_balance, self.account_balance])
