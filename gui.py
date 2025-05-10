
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QPushButton, QVBoxLayout, QLabel,
    QLineEdit, QMessageBox, QListWidget, QStackedWidget, QHBoxLayout
)
from PyQt6.QtGui import QDoubleValidator, QIntValidator
from storage import load_accounts, save_accounts
from account import RegularAccount, SavingAccount, Account
from utils import validate_amount, validate_name, validate_pin

class MainScreen(QWidget):
    '''
    This creates the main screen widget that allows users to view existing accounts,
    enter PIN and amount, perform deposit or withdrawal, and switch to account creation screen.
    '''

    def __init__(self, switch_to_create, deposit_cb, withdraw_cb):
        '''
        This initializes the main screen interface.
        '''
        super().__init__()
        layout = QVBoxLayout()

        self.account_list = QListWidget()
        self.pin_input = QLineEdit()
        self.pin_input.setPlaceholderText("Enter PIN")
        self.pin_input.setValidator(QIntValidator(0, 9999, self))
        self.pin_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("Enter amount")
        self.amount_input.setValidator(QDoubleValidator(0.01, 1e9, 2, self))

        self.deposit_button = QPushButton("Deposit")
        self.withdraw_button = QPushButton("Withdraw")
        self.create_button = QPushButton("Create Account")
        self.status_label = QLabel()

        layout.addWidget(QLabel("Accounts:"))
        layout.addWidget(self.account_list)
        layout.addWidget(QLabel("PIN:"))
        layout.addWidget(self.pin_input)
        layout.addWidget(QLabel("Amount:"))
        layout.addWidget(self.amount_input)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.deposit_button)
        btn_layout.addWidget(self.withdraw_button)
        btn_layout.addWidget(self.create_button)
        layout.addLayout(btn_layout)
        layout.addWidget(self.status_label)
        self.setLayout(layout)

        self.create_button.clicked.connect(switch_to_create)
        self.deposit_button.clicked.connect(deposit_cb)
        self.withdraw_button.clicked.connect(withdraw_cb)

class CreateAccountScreen(QWidget):
    '''
    This is the class for account creation screen.
    '''

    def __init__(self, create_cb, switch_back):
        '''
        This initializes the account creation interface.
        '''
        super().__init__()
        layout = QVBoxLayout()
        self.name_input = QLineEdit()
        self.pin_input = QLineEdit()
        self.pin_input.setPlaceholderText("4-digit PIN")
        self.pin_input.setValidator(QIntValidator(0, 9999, self))
        self.pin_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.reg_button = QPushButton("Create Regular Account")
        self.sav_button = QPushButton("Create Saving Account")
        self.back_button = QPushButton("Back to Main")
        self.status_label = QLabel()

        layout.addWidget(QLabel("Name:"))
        layout.addWidget(self.name_input)
        layout.addWidget(QLabel("PIN:"))
        layout.addWidget(self.pin_input)
        layout.addWidget(self.reg_button)
        layout.addWidget(self.sav_button)
        layout.addWidget(self.back_button)
        layout.addWidget(self.status_label)
        self.setLayout(layout)

        self.reg_button.clicked.connect(lambda: create_cb(self.name_input.text(), self.pin_input.text(), False, self.status_label))
        self.sav_button.clicked.connect(lambda: create_cb(self.name_input.text(), self.pin_input.text(), True, self.status_label))
        self.back_button.clicked.connect(switch_back)

class BankApp(QMainWindow):
    '''
    This is the main window that manages the bank account application using PyQt6.
    '''

    def __init__(self):
        '''
        This initializes the bank app, loads accounts, and sets up screens.
        '''
        super().__init__()
        self.setWindowTitle("Bank Account Manager")
        try:
            self.accounts = load_accounts()
        except IOError as e:
            QMessageBox.critical(self, "Error", str(e))
            self.accounts = []

        self.stack = QStackedWidget()
        self.main_screen = MainScreen(self.show_create, self._deposit, self._withdraw)
        self.create_screen = CreateAccountScreen(self._create_account, self.show_main)
        self.stack.addWidget(self.main_screen)
        self.stack.addWidget(self.create_screen)
        self.setCentralWidget(self.stack)
        self._refresh_main()

    def show_create(self):
        '''
        This switches to the account creation screen and clears inputs.
        '''
        self.create_screen.status_label.clear()
        self.create_screen.name_input.clear()
        self.create_screen.pin_input.clear()
        self.stack.setCurrentWidget(self.create_screen)

    def show_main(self):
        '''
        This returns to the main screen and refreshes the account list.
        '''
        self.stack.setCurrentWidget(self.main_screen)
        self._refresh_main()

    def _get_selected_account(self) -> Account | None:
        '''
        This retrives currently selected account from the list.
        '''
        idx = self.main_screen.account_list.currentRow()
        if 0 <= idx < len(self.accounts):
            return self.accounts[idx]
        return None

    def _create_account(self, name: str, pin: str, saving: bool, status_label: QLabel):
        '''
        This validates the input and creates a new account.
        '''
        try:
            valid_name = validate_name(name)
            valid_pin = validate_pin(pin)
            acc = SavingAccount(valid_name, valid_pin) if saving else RegularAccount(valid_name, valid_pin)
            self.accounts.append(acc)
            status_label.setText(f"{"Saving" if saving else "Regular"}" + f" account '{valid_name}' created.")
        except ValueError as e:
            status_label.setText(str(e))

    def _verify_and_perform(self, action: str):
        '''
        This performs deposit or withdrawal after verifying account and PIN.
        '''
        acc = self._get_selected_account()
        if not acc:
            self.main_screen.status_label.setText("Select an account.")
            return
        pin = self.main_screen.pin_input.text()
        if not acc.check_pin(pin):
            self.main_screen.status_label.setText("Invalid PIN.")
            return
        try:
            amount = validate_amount(self.main_screen.amount_input.text())
        except ValueError as e:
            QMessageBox.warning(self, "Invalid Input", str(e))
            return
        if action == 'deposit':
            success = acc.deposit(amount)
            msg = f"Deposited ${amount:.2f}" if success else "Deposit failed"
        else:
            success = acc.withdraw(amount)
            msg = f"Withdrew ${amount:.2f}" if success else "Withdrawal failed"
        if success:
            self._refresh_main()
        self.main_screen.status_label.setText(msg + f" {'to' if action=='deposit' else 'from'} '{acc.get_name()}'.")

    def _deposit(self):
        '''
        This initiates a deposit operation for the selected account.
        '''
        self._verify_and_perform('deposit')

    def _withdraw(self):
        '''
        This initiates a withdrawal operation for the selected account.
        '''
        self._verify_and_perform('withdraw')

    def _refresh_main(self) -> None:
        '''
        This updates the account list display and saves the current accounts.
        '''
        self.main_screen.account_list.clear()
        for acc in self.accounts:
            self.main_screen.account_list.addItem(str(acc))
        save_accounts(self.accounts)