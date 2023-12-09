import tkinter as tk
import gui
from accounts import Account, SavingAccount


def open_main_account_window():
    """Opens the main account window using gui module, creates account for 'Jane'"""

    account = Account("Jane")
    gui.open_main_account_window(account)


if __name__ == "__main__":
    root = tk.Tk()
    select_label = tk.Label(root, text="Select an option:")
    select_label.pack()

    select_box = tk.Listbox(root)
    select_box.insert(1, "Jane")
    select_box.pack()

    open_button = tk.Button(root, text="Open Main Account Window", command=open_main_account_window)
    open_button.pack()

    root.mainloop()
