from typing import Optional, Dict, List
from dataclasses import dataclass, field
from datetime import datetime
import re

# Descriptor for validating strings
class ValidString:
    """Descriptor for string validation."""
    
    def __init__(self, minlen: int = 1, maxlen: Optional[int] = None, pattern: Optional[str] = None):
        self.minlen = minlen
        self.maxlen = maxlen
        self.pattern = re.compile(pattern) if pattern else None
    
    def __get__(self, obj, objtype=None):
        if not obj:
            return self
        return obj.__dict__.get(f"_{self.name}", "")
    
    def __set__(self, obj, value: str):
        if not isinstance(value, str):
            raise TypeError("Value must be a string")
        
        if len(value) < self.minlen:
            raise ValueError(f"String must be at least {self.minlen} characters")
        
        if self.maxlen and len(value) > self.maxlen:
            raise ValueError(f"String must be at most {self.maxlen} characters")
        
        if self.pattern and not self.pattern.match(value):
            raise ValueError("String does not match required pattern")
        
        obj.__dict__[f"_{self.name}"] = value
    
    def __set_name__(self, owner, name):
        self.name = name

# Descriptor for validating numbers
class ValidNumber:
    """Descriptor for number validation."""
    
    def __init__(self, min_value: Optional[float] = None, max_value: Optional[float] = None):
        self.min_value = min_value
        self.max_value = max_value
    
    def __get__(self, obj, objtype=None):
        if not obj:
            return self
        return obj.__dict__.get(f"_{self.name}", 0)
    
    def __set__(self, obj, value: float):
        if not isinstance(value, (int, float)):
            raise TypeError("Value must be a number")
        
        if self.min_value is not None and value < self.min_value:
            raise ValueError(f"Value must be at least {self.min_value}")
        
        if self.max_value is not None and value > self.max_value:
            raise ValueError(f"Value must be at most {self.max_value}")
        
        obj.__dict__[f"_{self.name}"] = value
    
    def __set_name__(self, owner, name):
        self.name = name

@dataclass
class Transaction:
    """Represents a bank account transaction."""
    date: datetime
    description: str
    amount: float
    balance: float

class BankAccount:
    """Bank account with validation."""
    
    # Descriptors for validation
    account_number = ValidString(minlen=10, maxlen=10, pattern=r'^\d{10}$')
    holder_name = ValidString(minlen=2, maxlen=50, pattern=r'^[A-Za-z\s\'-]+$')
    balance = ValidNumber(min_value=0)
    
    def __init__(self, account_number: str, holder_name: str, initial_balance: float = 0):
        self.account_number = account_number
        self.holder_name = holder_name
        self._transactions: List[Transaction] = []
        self.balance = initial_balance
        self._add_transaction("Initial deposit", initial_balance)
    
    def _add_transaction(self, description: str, amount: float) -> None:
        """Add a transaction to the history."""
        transaction = Transaction(
            date=datetime.now(),
            description=description,
            amount=amount,
            balance=self.balance
        )
        self._transactions.append(transaction)
    
    def deposit(self, amount: float) -> None:
        """Deposit money into the account."""
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        
        self.balance += amount
        self._add_transaction("Deposit", amount)
    
    def withdraw(self, amount: float) -> None:
        """Withdraw money from the account."""
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        
        self.balance -= amount
        self._add_transaction("Withdrawal", -amount)
    
    @property
    def transaction_history(self) -> List[Transaction]:
        """Get the transaction history (read-only)."""
        return self._transactions.copy()
    
    def print_statement(self) -> None:
        """Print the account statement."""
        print(f"\nAccount Statement for {self.holder_name}")
        print(f"Account Number: {self.account_number}")
        print("\nTransactions:")
        print("Date                 Description          Amount     Balance")
        print("-" * 60)
        
        for t in self._transactions:
            print(f"{t.date:%Y-%m-%d %H:%M:%S} {t.description:<20} {t.amount:>8.2f} {t.balance:>10.2f}")

class Bank:
    """Bank class to manage multiple accounts."""
    
    def __init__(self, name: str):
        self.name = name
        self._accounts: Dict[str, BankAccount] = {}
    
    def create_account(self, account_number: str, holder_name: str, initial_balance: float = 0) -> BankAccount:
        """Create a new bank account."""
        if account_number in self._accounts:
            raise ValueError("Account number already exists")
        
        account = BankAccount(account_number, holder_name, initial_balance)
        self._accounts[account_number] = account
        return account
    
    def get_account(self, account_number: str) -> BankAccount:
        """Get an account by its number."""
        if account_number not in self._accounts:
            raise ValueError("Account not found")
        return self._accounts[account_number]
    
    def transfer(self, from_account: str, to_account: str, amount: float) -> None:
        """Transfer money between accounts."""
        source = self.get_account(from_account)
        destination = self.get_account(to_account)
        
        # This will raise ValueError if insufficient funds
        source.withdraw(amount)
        destination.deposit(amount)

def main():
    # Create a bank
    bank = Bank("Python Bank")
    
    try:
        # Create some accounts
        account1 = bank.create_account("1234567890", "John Doe", 1000)
        account2 = bank.create_account("9876543210", "Jane Smith", 500)
        
        # Perform some transactions
        account1.deposit(500)
        account1.withdraw(200)
        bank.transfer("1234567890", "9876543210", 300)
        
        # Print statements
        account1.print_statement()
        account2.print_statement()
        
        # Demonstrate validation
        try:
            # This should fail - negative amount
            account1.withdraw(-100)
        except ValueError as e:
            print(f"\nValidation error: {e}")
        
        try:
            # This should fail - invalid account number
            bank.create_account("123", "Invalid", 100)
        except ValueError as e:
            print(f"Validation error: {e}")
        
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main() 