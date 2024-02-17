import tkinter as tk
from tkinter import messagebox
from coins import Account

def retrieve_balance():
    try:
        email = email_entry.get()
        token = token_entry.get()
        account = Account(email, token)
        balance = account.retrieve_balance()
        balance_label.config(text=f"Current Balance: {balance}")
    except AssertionError as e:
        messagebox.showerror("Error", str(e))

def transfer_coins():
    try:
        email = email_entry.get()
        token = token_entry.get()
        account = Account(email, token)
        recipient_email = recipient_email_entry.get()
        amount = int(amount_entry.get())
        message = account.transfer(amount, recipient_email)
        messagebox.showinfo("Transfer Successful", message)
        retrieve_balance()  # Update balance display
    except AssertionError as e:
        messagebox.showerror("Error", str(e))

app = tk.Tk()
app.title("Coins Account Manager")

tk.Label(app, text="Email:").pack()
email_entry = tk.Entry(app)
email_entry.pack()

tk.Label(app, text="Token:").pack()
token_entry = tk.Entry(app)
token_entry.pack()

tk.Label(app, text="Recipient Email:").pack()
recipient_email_entry = tk.Entry(app)
recipient_email_entry.pack()

tk.Label(app, text="Amount:").pack()
amount_entry = tk.Entry(app)
amount_entry.pack()

balance_label = tk.Label(app, text="Current Balance: Unknown")
balance_label.pack()

tk.Button(app, text="Retrieve Balance", command=retrieve_balance).pack()
tk.Button(app, text="Transfer Coins", command=transfer_coins).pack()

app.mainloop()
