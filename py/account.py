import os

class Account:
    def __init__(self) -> None:
        self.balance = 0

    def deposit(self, amount: int, *args, **kwargs) -> int:
        self.balance += amount
        return self.balance
    
    def withdraw(self, amount: int, *args, **kwargs) -> int:
        if self.balance >= amount:
            self.balance -= amount
            return amount
        amount_available = self.balance
        self.balance = 0
        return amount_available
    
    def get_balance(self) -> int:
        return self.balance
    
def create_acct(initial_amount: int=0) -> Account:
    acct = Account()
    acct.deposit(initial_amount)
    return acct