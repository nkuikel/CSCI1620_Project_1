import csv
from pathlib import Path
from typing import List
from account import RegularAccount, SavingAccount, Account

# This defines the path to the CSV file for storing account data.
CSV_PATH = Path(__file__).parent / "data.csv"

def load_accounts() -> List[Account]:
    '''
    This loads account data from the CSV file and returns a list of Account objects.
    '''
    accounts: List[Account] = []
    if not CSV_PATH.exists():
        return accounts

    try:
        with CSV_PATH.open(mode="r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                name = row.get("name", "")
                pin = row.get("pin", "")

                # Attempt to parse balance, default to 0.0 on failure
                try:
                    balance = float(row.get("balance", 0))
                except ValueError:
                    balance = 0.0

                acc_type = row.get("type", "Regular")

                # Create the correct account type and set its balance
                if acc_type == "Saving":
                    acc = SavingAccount(name, pin)
                else:
                    acc = RegularAccount(name, pin)
                    acc.set_balance(balance)

                accounts.append(acc)
    except Exception as e:
        raise IOError(f"Failed to load accounts: {e}")

    return accounts

def save_accounts(accounts: List[Account]) -> None:
    '''
    This saves the current list of accounts to the CSV file.
    '''
    try:
        with CSV_PATH.open(mode="w", newline="") as file:
            fieldnames = ["type", "name", "balance", "pin"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

            for acc in accounts:
                acc_type = "Saving" if isinstance(acc, SavingAccount) else "Regular"

                # Write account data to CSV
                writer.writerow({
                    "type": acc_type,
                    "name": acc.get_name(),
                    "balance": f"{acc.get_balance():.2f}",
                    "pin": acc._pin  # Accessing protected member is acceptable in this controlled context
                })
    except Exception as e:
        raise IOError(f"Failed to save accounts: {e}")
