from abc import ABC, abstractmethod

class Account(ABC):
    '''
    This is an abstract base class for bank accounts.
    '''
    def __init__(self, name: str, pin: str, balance: float = 0.0) -> None:
        '''
        This initializes an account with name, pin, and optional balance.
        '''
        self._account_name: str = name
        self._pin: str = pin
        self._account_balance: float = 0.0
        self.set_balance(balance)

    @abstractmethod
    def deposit(self, amount: float) -> bool:
        '''
        This is an abstract method to deposit funds into the account.
        '''
        pass

    @abstractmethod
    def withdraw(self, amount: float) -> bool:
        '''
        This is an abstract method to withdraw funds from the account.
        '''
        pass

    def check_pin(self, pin: str) -> bool:
        '''
        This checks if the provided PIN is correct.
        '''
        return self._pin == pin

    def get_balance(self) -> float:
        '''
        This returns the current account balance.
        '''
        return self._account_balance

    def get_name(self) -> str:
        '''
        This returns the account holder's name.
        '''
        return self._account_name

    def set_balance(self, value: float) -> None:
        '''
        This sets the account balance to a non-negative value.
        '''
        self._account_balance = max(0.0, value)

    def set_name(self, value: str) -> None:
        '''
        This sets the account holder's name.
        '''
        self._account_name = value

    def __str__(self) -> str:
        '''
        This returns a string representation of the account.
        '''
        return f"{self.__class__.__name__}(Name={self.get_name()}, Balance=${self.get_balance():.2f})"


class RegularAccount(Account):
    '''
    This is a concrete implementation of a standard checking account.
    Allows full withdrawal up to the total balance.
    '''
    def deposit(self, amount: float) -> bool:
        '''
        This deposits a positive amount into the account.
        '''
        if amount <= 0:
            return False
        self._account_balance += amount
        return True

    def withdraw(self, amount: float) -> bool:
        '''
        This withdraws an amount if sufficient balance is available.
        '''
        if 0 < amount <= self._account_balance:
            self._account_balance -= amount
            return True
        return False


class SavingAccount(Account):
    '''
    This is a savings account with a minimum balance requirement and interest bonus.
    '''
    MINIMUM: float = 100.0
    RATE: float = 0.02

    def __init__(self, name: str, pin: str) -> None:
        '''
        This initializes a savings account with minimum balance.
        '''
        super().__init__(name, pin, SavingAccount.MINIMUM)
        self._deposit_count: int = 0

    def deposit(self, amount: float) -> bool:
        '''
        This deposits a positive amount and applies interest every 5th deposit.
        '''
        if amount <= 0:
            return False
        self._deposit_count += 1
        self._account_balance += amount

        # Apply interest every 5th deposit
        if self._deposit_count % 5 == 0:
            self._apply_interest()
        return True

    def withdraw(self, amount: float) -> bool:
        '''
        This withdraws an amount only if the resulting balance stays above the minimum.
        '''
        if amount <= 0 or self._account_balance - amount < SavingAccount.MINIMUM:
            return False
        self._account_balance -= amount
        return True

    def _apply_interest(self) -> None:
        '''
        This applies interest to the current balance.
        '''
        interest = self._account_balance * SavingAccount.RATE
        self._account_balance += interest

    def set_balance(self, value: float) -> None:
        '''
        This overrides set_balance to enforce the minimum balance.
        '''
        super().set_balance(max(value, SavingAccount.MINIMUM))
