import tkinter as tk
from accounts import Account, SavingAccount
import csv


def validate_float_input(action, value_if_allowed):
    """
    Validates float input in the entry widget
    Arguments:
    - action (str): the action being preformed
    - value_if_allowed (str): value being entered or edited
    Returns:
    - Bool: if True the input is valid, otherwise False:
    """
    # Function to validate float input in Entry widget
    if action == '1':  # Insertion (typing or pasting)
        try:
            float(value_if_allowed)
            return True
        except ValueError:
            # Show a popup message informing the user to input only numbers
            messagebox.showwarning("Invalid Input", "Please enter numbers only.")
            return False
    else:  # Deletion, backspace, etc.
        return True


class MainWindow:
    """
    Represents the main account window
    Attributes:
        - master: tkinter root for the window
        - account: instance of the account class
    """
    def __init__(self, master, account):
        self.master = master
        self.account = account

        self.master.title("Main Account Window")

        self.balance_label = tk.Label(self.master, text=f"Balance: ${self.account.get_balance():.2f}")
        self.balance_label.pack()

        self.amount_entry = tk.Entry(self.master)
        self.amount_entry.pack()

        self.deposit_button = tk.Button(self.master, text="Deposit", command=self.deposit)
        self.deposit_button.pack()

        self.withdraw_button = tk.Button(self.master, text="Withdraw", command=self.withdraw)
        self.withdraw_button.pack()

        self.savings_button = tk.Button(self.master, text="Open Savings Account", command=self.open_savings_window)
        self.savings_button.pack()

        self.back_button = tk.Button(self.master, text="Back to Tk Window", command=self.back_to_tk_window)
        self.back_button.pack()

    def deposit(self):
        amount = self.amount_entry.get()
        try:
            amount = float(amount)
            self.account.deposit(amount)
            self.update_balance()
        except ValueError:
            messagebox.showwarning("Invalid Input", "Please enter numbers only.")

    def withdraw(self):
        amount = self.amount_entry.get()
        try:
            amount = float(amount)
            self.account.withdraw(amount)
            self.update_balance()
        except ValueError:
            messagebox.showwarning("Invalid Input", "Please enter numbers only.")

    def update_balance(self):
        # Update balance label or other GUI elements with account balance
        pass

    def update_balance(self):
        self.balance_label.config(text=f"Balance: ${self.account.get_balance():.2f}")

    def update_csv(self):
        with open("User_Statements.csv", 'a', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(
                ['Main Account', 'Deposit/Withdraw', self.amount_entry.get(), self.main_account.get_balance()])

    def open_savings_window(self):
        self.master.withdraw()
        savings_account = SavingAccount(self.account.get_name())
        savings_root = tk.Tk()
        savings_window = SavingsWindow(savings_root, savings_account, self)
        savings_root.mainloop()

    def back_to_tk_window(self):
        self.master.withdraw()  # Hide the main account window
        root.deiconify()


class SavingsWindow:
    """
    Represents the savings account window
    Attributes:
        - master: tkinter root for the window
        - savings_account: instance of the SavingAccount class
        - main_window: instance of the MainWindow class
    """
    def __init__(self, master, savings_account, main_window):
        self.master = master
        self.savings_account = savings_account
        self.main_window = main_window

        self.master.title("Savings Account Window")
        self.balance_label = tk.Label(self.master,
                                      text=f"Savings Account Balance: ${self.savings_account.get_balance():.2f}")
        self.balance_label.pack()

        self.amount_entry = tk.Entry(self.master)
        self.amount_entry.pack()

        self.deposit_button = tk.Button(self.master, text="Deposit", command=self.deposit)
        self.deposit_button.pack()

        self.withdraw_button = tk.Button(self.master, text="Withdraw", command=self.withdraw)
        self.withdraw_button.pack()

        self.back_button = tk.Button(self.master, text="Back to Main Account", command=self.back_to_main)
        self.back_button.pack()

    def deposit(self):
        amount = float(self.amount_entry.get())
        if self.savings_account.deposit(amount):
            self.update_balance()

    def withdraw(self):
        amount = float(self.amount_entry.get())
        if self.savings_account.withdraw(amount):
            self.update_balance()

    def update_balance(self):
        self.balance_label.config(text=f"Savings Account Balance: ${self.savings_account.get_balance():.2f}")

    def back_to_main(self):
        global account_window_open
        account_window_open = False  # Set the flag to False when the window is closed
        self.master.destroy()  # Close the current savings window
        self.main_window.master.deiconify()


def open_main_account_window(account):
    """
    Opens the main account window
    Arguments:
    - account: instance of the Account class
    Returns:
    - None
    """
    root = tk.Tk()
    main_window = MainWindow(root, account)
    root.mainloop()
