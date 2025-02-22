import random
import json
import os

class ATM:
    def __init__(self, name, initial_balance, pin):
        self.name = name
        self.balance = initial_balance
        self.pin = pin

    def validate_pin(self, entered_pin):
        return self.pin == entered_pin

    def deposit(self, amount):
        self.balance += amount
        self.save_transaction_history("Deposit", amount)
        self.save_account_details()
        return self.balance

    def withdraw(self, amount):
        while amount > self.balance:
            print("Withdrawal amount should not exceed the current balance.")
            amount = float(input("Enter a valid Withdrawal Amount: "))
        self.balance -= amount
        self.save_transaction_history("Withdraw", amount)
        self.save_account_details()
        return self.balance

    def save_transaction_history(self, transaction_type, amount):
        if os.path.exists("transaction_data.json"):
            with open("transaction_data.json", "r") as file:
                transaction_data = json.load(file)
        else:
            transaction_data = {}

        if self.name not in transaction_data:
            transaction_data[self.name] = []

        transaction_data[self.name].append({
            "Type": transaction_type,
            "Amount": amount,
            "Balance": self.balance
        })

        with open("transaction_data.json", "w") as file:
            json.dump(transaction_data, file, indent=4)

    def save_account_details(self):
        if os.path.exists("user_data.json"):
            with open("user_data.json", "r") as file:
                user_data = json.load(file)
        else:
            user_data = {}

        user_data[self.name] = {
            "Balance": self.balance,
            "PIN": self.pin
        }

        with open("user_data.json", "w") as file:
            json.dump(user_data, file, indent=4)

    def get_account_balance(self):
        return self.balance

    def get_transaction_history(self):
        if os.path.exists("transaction_data.json"):
            with open("transaction_data.json", "r") as file:
                transaction_data = json.load(file)
            return transaction_data.get(self.name, [])
        return []


def generate_otp():
    return random.randint(100000, 999999)

def validate_otp(sent_otp):
    entered_otp = int(input("Enter the OTP sent to your registered number: "))
    return sent_otp == entered_otp

def create_or_login():
    name = input("Enter Name: ")

    if os.path.exists("user_data.json"):
        with open("user_data.json", "r") as file:
            user_data = json.load(file)
        if name in user_data:
            print(f"Welcome back, {name}!")
            return name, user_data[name]["Balance"], user_data[name]["PIN"]
        else:
            print(f"User {name} not found. Proceeding with account creation.")
    else:
        print("No users found. Proceeding with account creation.")

    initial_balance = float(input("Enter Your Balance: "))
    while initial_balance <= 0:
        print("Balance should be greater than 0.")
        initial_balance = float(input("Enter Your Balance: "))

    pin = input("Set Your PIN (4-digit): ")
    while len(pin) != 4 or not pin.isdigit():
        print("Invalid PIN. Enter a 4-digit numeric PIN.")
        pin = input("Set Your PIN (4-digit): ")

    otp = generate_otp()
    print(f"OTP for account creation is: {otp}")

    if not validate_otp(otp):
        print("OTP verification failed. Account creation aborted.")
        exit()

    return name, initial_balance, pin


name, initial_balance, pin = create_or_login()
atm = ATM(name, initial_balance, pin)

if name not in os.listdir():
    atm.save_account_details()

while True:
    entered_pin = input("Enter Your PIN: ")
    if atm.validate_pin(entered_pin):
        print(f"Welcome {atm.name}!")
        while True:
            print("\nOptions:")
            print("1. Deposit")
            print("2. Withdraw")
            print("3. View Transaction History")
            print("4. Exit")
            choice = input("Enter your choice: ")

            if choice == "1":
                deposit_amount = float(input("Enter the amount to deposit: "))
                atm.deposit(deposit_amount)
                print(f"Your current balance is: {atm.get_account_balance()}")

            elif choice == "2":
                withdrawal_amount = float(input("Enter the amount to withdraw: "))
                atm.withdraw(withdrawal_amount)
                print(f"Your current balance is: {atm.get_account_balance()}")

            elif choice == "3":
                transactions = atm.get_transaction_history()
                if transactions:
                    print("\nTransaction History:")
                    for index, transaction in enumerate(transactions, start=1):
                        print(f"{index}. {transaction['Type']} - Amount: {transaction['Amount']} - Balance: {transaction['Balance']}")
                else:
                    print("No transactions available.")

            elif choice == "4":
                print("Thank you visit again bye!")
                break
            else:
                print("Invalid choice. Please try again.")
        break
    else:
        print("Incorrect PIN. Please try again.")