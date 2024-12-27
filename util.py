import os
from main import main
num7 = 0

def get_valid_bet(money):
    while True:
        try:
            bet = float(input(f"Enter your bet amount (You have ${money:.2f}): "))
            if bet > money:
                print("You cannot bet more than you have!")
            elif bet < 0:
                print("Your bet must be greater than 0!")
                num7 += 1
            elif bet == 0:
                print("Exiting game...")
                main()
            else:
                return bet
        except ValueError:
            print("Invalid input. Please enter a numeric value.")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
