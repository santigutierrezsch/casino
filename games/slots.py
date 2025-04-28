import random
import time
import sys
import os
from util import get_valid_bet, clear_screen

def spinning_animation(duration=2, width=40):
    """Create a spinning animation for the slot machine"""
    symbols = ["🍒", "🍋", "🍉", "⭐", "💎", "7️⃣", "🍇", "🔔"]
    
    start_time = time.time()
    while time.time() - start_time < duration:
        # Generate random symbols for each reel
        reels = []
        for _ in range(3):
            reels.append(random.choice(symbols))
        
        # Display the spinning reels
        sys.stdout.write("\r" + " " * width)
        sys.stdout.write(f"\r   {reels[0]} | {reels[1]} | {reels[2]}   ")
        sys.stdout.flush()
        
        # Brief pause between animations
        time.sleep(0.1)
    
    # Return to beginning of line
    sys.stdout.write("\r" + " " * width + "\r")
    sys.stdout.flush()

def display_winning_animation(result):
    """Display a special animation for winning combinations"""
    
    for _ in range(3):
        # Flash the winning combination
        time.sleep(0.3)
        sys.stdout.write("\r    " + "   ".join(["✨"] * len(result)) + "    ")
        sys.stdout.flush()
        time.sleep(0.3)
        sys.stdout.write("\r    " + "   ".join(result) + "    ")
        sys.stdout.flush()
    
    print("\n🎰 WINNER! 🎰")

    # Final newline
    print()

def calculate_winnings(bet, result):
    """Calculate winnings based on the combination"""
    # All three symbols match (Jackpot)
    if result[0] == result[1] == result[2]:
        if result[0] == "💎":
            return bet * 100  # Diamond jackpot pays 100x
        elif result[0] == "7️⃣":
            return bet * 77   # Lucky 7 pays 77x
        else:
            return bet * 50   # Regular jackpot pays 50x
    
    # Two matching symbols in a row
    if result[0] == result[1] or result[1] == result[2]:
        return bet * 3  # Two matching symbols pays 3x
        
    # Special case for cherries (only if no other matches)
    if "🍒" in result and not (result[0] == result[1] or result[1] == result[2]):
        cherry_count = result.count("🍒")
        if cherry_count >= 2:
            return bet * 2    # Two or more cherries pays 2x
    
    return 0  # No win

def check_win_type(result):
    """Return a description of the win type for display purposes"""
    if result[0] == result[1] == result[2]:
        return "JACKPOT! Three matching symbols!"
    
    if result[0] == result[1]:
        return f"Two {result[0]}s in a row!"
    
    if result[1] == result[2]:
        return f"Two {result[1]}s in a row!"
    
    cherry_count = result.count("🍒")
    if cherry_count >= 2:
        return f"{cherry_count} cherries - small win!"
        
    return "No winning combination"

def play(player):
    clear_screen()
    print("\n--- Welcome to Slots ---")
    
    current_bet = get_valid_bet(player.get_balance())
    if current_bet == 0:  # User wants to exit
        return
        
    keep_playing = True
    
    while keep_playing and player.get_balance() > 0:
        # Check if the player has enough balance for the current bet
        if current_bet > player.get_balance():
            print(f"Your current bet (${current_bet:.2f}) exceeds your balance.")
            current_bet = get_valid_bet(player.get_balance())
            if current_bet == 0:  # User wants to exit
                return
        
        # Deduct the bet amount
        if not player.deduct_balance(current_bet):
            return
            
        print(f"\nBet amount: ${current_bet:.2f}")
        print("Spinning the reels...")
        
        # Show spinning animation
        spinning_animation()
        
        # Generate the result
        symbols = ["🍒", "🍋", "🍉", "⭐", "💎", "7️⃣", "🍇", "🔔"]
        # Weights make some symbols rarer than others
        weights = [20, 20, 15, 10, 5, 3, 15, 12]
        result = [random.choices(symbols, weights)[0] for _ in range(3)]
        
        # Display the result (only once)
        print(f"\n{result[0]} | {result[1]} | {result[2]}")
        
        # Calculate and apply winnings
        winnings = calculate_winnings(current_bet, result)
        win_type = check_win_type(result)
        
        if winnings > 0:
            # Show winning animation for any win
            display_winning_animation(result)
            
            # Display win type for clarity
            print(win_type)
            
            if winnings >= current_bet * 20:
                print(f"💰 MAJOR WIN! You win ${winnings:.2f}! 💰")
            else:
                print(f"You win ${winnings:.2f}!")
                
            player.add_balance(winnings)
        else:
            print("No winning combination. Better luck next time!")
        
        print(f"\nYour current balance: ${player.get_balance():.2f}")
        
        # Check if the player has enough balance to continue
        if player.get_balance() < 0.01:
            print("You've run out of funds. Game over!")
            keep_playing = False
            continue
            
        # Prompt for next action
        print("\nOptions:")
        print("- Press ENTER to play again with the same bet")
        print("- Type 'C' to change your bet")
        print("- Type 'E' to exit")
        
        choice = input("Your choice: ").strip().upper()
        
        if choice == 'E':
            keep_playing = False
        elif choice == 'C':
            current_bet = get_valid_bet(player.get_balance())
            if current_bet == 0:  # User wants to exit
                return
        elif choice == '':
            # Continue with same bet (Enter pressed)
            pass
        else:
            print("Invalid choice. Playing again with the same bet.")
            time.sleep(1)
        
        clear_screen()
        
    print("\nThanks for playing Slots!")