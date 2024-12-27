from config import STARTING_BALANCE
from games import baccarat, blackjack, poker, roulette, slots
from player import Player
from util import clear_screen, get_valid_bet

FALLBACK_NAME = "Player"

def display_menu():
    print("\n--- Welcome to the Digital Casino ---")
    print("1. Play Blackjack")
    print("2. Play Roulette")
    print("3. Play Slots")
    print("4. Play Poker")
    print("5. Play Baccarat")
    print("6. Check Wallet")
    print("7. Exit")

def get_starting_balance():
    special_code = "7407150709"
    code = input("Enter special code for custom starting balance (or press Enter to skip): ").strip()
    if code == special_code:
        while True:
            try:
                balance = float(input("Enter your starting balance: "))
                if balance <= 0:
                    print("Starting balance must be greater than 0!")
                    continue
                if balance > 0:
                    return balance
                else:
                    print("Starting balance must be greater than 0!")
            except ValueError:
                print("Invalid input. Please enter a numeric value.")
    print(f"Using default starting balance of ${STARTING_BALANCE:.2f}")
    return STARTING_BALANCE

def main():
    clear_screen()
    name = input("Enter your name: ").strip().title()
    if not name:
        name = FALLBACK_NAME  # Fallback to default name if none is entered
    starting_balance = get_starting_balance()
    player = Player(balance=starting_balance, name=name)

   
    while True:
        display_menu()
        choice = input("Choose a game (1-7): ").strip()
        while choice not in {"1", "2", "3", "4", "5", "6", "7"}:
            print("Invalid choice. Please select a valid option (1-7).")
            choice = input("Choose a game (1-7): ").strip()

        if choice == "1":
            blackjack.play(player)
        elif choice == "2":
            roulette.play(player)
        elif choice == "3":
            slots.play(player)
        elif choice == "4":
            poker.play(player)
        elif choice == "5":
            baccarat.play(player)
        elif choice == "6":
            print(f"Your wallet balance: ${player.get_balance():.2f}")
        elif choice == "7":
            print(f"Thanks for playing, {player.name}! Your final balance is ${player.get_balance():.2f}. Goodbye!")
            break
        else:
            print("Invalid choice. Please select a valid option (1-6).")
        
        # Pause before redisplaying the menu to allow the player to see the result of their action
        input("Press Enter to continue...")
        clear_screen()
    clear_screen()

if __name__ == "__main__":
    main()