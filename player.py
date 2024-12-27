class Player:
    def __init__(self, balance, name="Player"):
        self.balance = balance
        self.hand = []
        self.bet = 0
        self.name = name

    def deduct_balance(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            return True
        else:
            print("Insufficient balance.")
            return False

    def add_balance(self, amount):
        self.balance += amount

    def get_balance(self):
        return self.balance

    def choose_action(self, pot, current_bet):
        while True:
            action = input(
                f"{self.name}, choose your action: [call, raise, fold]: "
            ).strip().lower()

            if action == "raise":
                try:
                    raise_amount = float(input("Enter raise amount: ").strip())
                    if raise_amount > self.balance:
                        print("You don't have enough balance to raise.")
                    elif raise_amount <= current_bet:
                        print(f"Raise must exceed the current bet of ${current_bet}.")
                    else:
                        return action, raise_amount
                except ValueError:
                    print("Invalid input. Please enter a numeric value.")
            elif action == "call":
                if current_bet > self.balance:
                    print("You don't have enough balance to call.")
                    return "fold", 0
                return action, current_bet
            elif action == "fold":
                return action, 0
            else:
                print("Invalid action. Please enter 'call', 'raise', or 'fold'.")