from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from coins import Account

class CoinsApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Coins Account Manager')
        layout = QVBoxLayout()

        self.email_label = QLabel('Email:')
        self.email_entry = QLineEdit()
        layout.addWidget(self.email_label)
        layout.addWidget(self.email_entry)

        self.token_label = QLabel('Token:')
        self.token_entry = QLineEdit()
        layout.addWidget(self.token_label)
        layout.addWidget(self.token_entry)

        self.recipient_email_label = QLabel('Recipient Email:')
        self.recipient_email_entry = QLineEdit()
        layout.addWidget(self.recipient_email_label)
        layout.addWidget(self.recipient_email_entry)

        self.amount_label = QLabel('Amount:')
        self.amount_entry = QLineEdit()
        layout.addWidget(self.amount_label)
        layout.addWidget(self.amount_entry)

        self.balance_label = QLabel('Current Balance: Unknown')
        layout.addWidget(self.balance_label)

        self.retrieve_balance_button = QPushButton('Retrieve Balance')
        self.retrieve_balance_button.clicked.connect(self.retrieve_balance)
        layout.addWidget(self.retrieve_balance_button)

        self.transfer_coins_button = QPushButton('Transfer Coins')
        self.transfer_coins_button.clicked.connect(self.transfer_coins)
        layout.addWidget(self.transfer_coins_button)

        self.setLayout(layout)

    def retrieve_balance(self):
        try:
            email = self.email_entry.text()
            token = self.token_entry.text()
            account = Account(email, token)
            balance = account.retrieve_balance()
            self.balance_label.setText(f"Current Balance: {balance}")
        except AssertionError as e:
            QMessageBox.critical(self, "Error", str(e))

    def transfer_coins(self):
        try:
            email = self.email_entry.text()
            token = self.token_entry.text()
            account = Account(email, token)
            recipient_email = self.recipient_email_entry.text()
            amount = int(self.amount_entry.text())
            message = account.transfer(amount, recipient_email)
            QMessageBox.information(self, "Transfer Successful", message)
            self.retrieve_balance()  # Update balance display
        except AssertionError as e:
            QMessageBox.critical(self, "Error", str(e))

if __name__ == '__main__':
    app = QApplication([])
    ex = CoinsApp()
    ex.show()
    app.exec_()
