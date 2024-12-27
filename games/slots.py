import random
from util import get_valid_bet

def play(player):
    print("\n--- Welcome to Slots ---")
    bet = get_valid_bet(player.get_balance())
    if not player.deduct_balance(bet):
        return

    symbols = ["🍒", "🍋", "🍉", "⭐", "💎"]
    result = [random.choice(symbols) for _ in range(3)]
    print(" | ".join(result))

    if result[0] == result[1] == result[2]:
        winnings = bet * 50
        print(f"Jackpot! You win ${winnings:.2f}!")
        player.add_balance(winnings)
    else:
        print("Better luck next time!")