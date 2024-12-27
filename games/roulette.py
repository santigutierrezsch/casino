import random
from util import get_valid_bet
from itertools import chain

def play(player):
    print("\n--- Welcome to American Roulette ---")
    bet = get_valid_bet(player.get_balance())
    if not player.deduct_balance(bet):
        return

    print("\nBetting options:")
    print("1: Inside Bets (e.g., Straight, Split, Street, Corner)")
    print("2: Outside Bets (e.g., Red/Black, Odd/Even, High/Low)")

    wheel = list(chain(['0', '00'], (str(i) for i in range(1, 37))))
    colors = {  
        '0': 'green', '00': 'green',
        **{str(n): 'red' for n in [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]},
        **{str(n): 'black' for n in [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]},
    }

    spin_result = random.choice(wheel)
    spin_color = colors[spin_result]
    bet_type = None
    while bet_type not in [1, 2]:
        try:
            bet_type = int(input("Enter your choice (1 for Inside Bets, 2 for Outside Bets): "))
            if bet_type not in [1, 2]:
                print("Invalid choice. Choose 1 or 2.")
        except ValueError:
            print("Invalid input. Please enter 1 or 2.")

    if bet_type == 1:
        print("\nInside Bets:")
        print("1: Straight (specific number, payout 35:1)")
        print("2: Split (two adjacent numbers, payout 17:1)")
        print("3: Street (row of three numbers, payout 11:1)")
        print("4: Corner (four numbers forming a square, payout 8:1)")
        print("5: Advanced Inside Bets")

        while True:
            try:
                inside_choice = int(input("Enter your choice (1-5): "))
                if inside_choice not in range(1, 6):
                    print("Invalid choice. Choose a number between 1 and 5.")
                else:
                    break
            except ValueError:
                print("Invalid input. Please enter a number between 1 and 5.")

        if inside_choice == 1:  # Straight
            while True:
                chosen_number = input("Enter a number to bet on (0, 00, or 1-36): ").strip()
                if chosen_number in wheel:
                    break
                else:
                    print("Invalid number. Please enter 0, 00, or a number between 1 and 36.")
            winnings = bet * 35
            print(f"The wheel spun... Result: {spin_result} ({spin_color}).")
            print(f"You guessed the correct number! You win ${winnings:.2f}.")
            player.add_balance(winnings)

        elif inside_choice == 2:  # Split
            while True:
                num1 = input("Enter the first number in the split (0, 00, or 1-36): ").strip()
                if num1 in wheel:
                    break
                else:
                    print("Invalid number. Please enter a valid roulette number.")
            
            while True:
                num2 = input("Enter the second number in the split (0, 00, or 1-36): ").strip()
                if num2 in wheel:
                    break
                else:
                    print("Invalid number. Please enter a valid roulette number.")
            
            if spin_result in [num1, num2]:
                winnings = bet * 17
                print(f"The wheel spun... Result: {spin_result} ({spin_color}).")
                print(f"You guessed correctly! You win ${winnings:.2f}.")
                player.add_balance(winnings)
            else:
                print(f"The wheel spun... Result: {spin_result} ({spin_color}).")
                print("You lost your bet.")

        elif inside_choice == 3:  # Street
            row_start = int(input("Enter the starting number of the row (1, 4, 7, ..., 34): "))
            if spin_result in [str(row_start), str(row_start + 1), str(row_start + 2)]:
                winnings = bet * 11
                print(f"You guessed correctly! You win ${winnings:.2f}.")
                player.add_balance(winnings)
            else:
                print(f"The wheel spun... Result: {spin_result} ({spin_color}).")
                print("You lost your bet.")

        elif inside_choice == 4:  # Corner
            while True:
                nums = input("Enter the four numbers in the corner, separated by spaces: ").strip().split()
                if all(num in wheel for num in nums) and len(nums) == 4:
                    break
                else:
                    print("Invalid numbers. Please enter four valid roulette numbers.")
            if spin_result in nums:
                winnings = bet * 8
                print(f"The wheel spun... Result: {spin_result} ({spin_color}).")
                print(f"You guessed correctly! You win ${winnings:.2f}.")
                player.add_balance(winnings)
            else:
                print(f"The wheel spun... Result: {spin_result} ({spin_color}).")
                print("You lost your bet.")

        elif inside_choice == 5:  # Advanced Inside Bets
            print("Advanced Inside Bets:")
            print("1: Basket (0, 00, 1, 2, 3, payout 6:1)")
        elif inside_choice == 5:  # Advanced Inside Bets
            print("Advanced Inside Bets:")
            print("1: Basket (0, 00, 1, 2, 3, payout 6:1)")
            print("2: Six Line (two adjacent rows, payout 5:1)")

            while True:
                try:
                    advanced_choice = int(input("Enter your choice (1 or 2): "))
                    if advanced_choice in [1, 2]:
                        break
                    else:
                        print("Invalid choice. Choose 1 or 2.")
                except ValueError:
                    print("Invalid input. Please enter 1 or 2.")

            if advanced_choice == 1:  # Basket
                    print(f"You guessed correctly! You win ${winnings:.2f}.")
                    player.add_balance(winnings)
                else:
                    print(f"The wheel spun... Result: {spin_result} ({spin_color}).")
                    print("You lost your bet.")
            elif advanced_choice == 2:  # Six Line
                while True:
                    try:
                        row_start = int(input("Enter the starting number of the first row (1, 4, 7, ..., 31): "))
                        if row_start in range(1, 34, 3):
                            break
                        else:
                            print("Invalid starting number. Please enter 1, 4, 7, ..., 31.")
                    except ValueError:
                        print("Invalid input. Please enter a valid number.")
                
                if spin_result in [str(row_start), str(row_start + 1), str(row_start + 2),
                                   str(row_start + 3), str(row_start + 4), str(row_start + 5)]:
                    winnings = bet * 5
                    print(f"The wheel spun... Result: {spin_result} ({spin_color}).")
                    print(f"You guessed correctly! You win ${winnings:.2f}.")
                    player.add_balance(winnings)
                else:
                    print(f"The wheel spun... Result: {spin_result} ({spin_color}).")
                    print("You lost your bet.")
                while True:
                    try:
                        row_start = int(input("Enter the starting number of the first row (1, 4, 7, ..., 31): "))
                        if row_start in range(1, 34, 3):
                            break
                        else:
                            print("Invalid starting number. Please enter 1, 4, 7, ..., 31.")
                    except ValueError:
                        print("Invalid input. Please enter a valid number.")
                
                if spin_result in [str(row_start), str(row_start + 1), str(row_start + 2),
                                   str(row_start + 3), str(row_start + 4), str(row_start + 5)]:
                    winnings = bet * 5
                    print(f"The wheel spun... Result: {spin_result} ({spin_color}).")
                    print(f"You guessed correctly! You win ${winnings:.2f}.")
                    player.add_balance(winnings)
                else:
                    print(f"The wheel spun... Result: {spin_result} ({spin_color}).")
                    print("You lost your bet.")

            if advanced_choice == 1:  # Basket
                if spin_result in ['0', '00', '1', '2', '3']:
                    winnings = bet * 6
                    print(f"The wheel spun... Result: {spin_result} ({spin_color}).")
                    print(f"You guessed correctly! You win ${winnings:.2f}.")
                    player.add_balance(winnings)
                else:
                    print(f"The wheel spun... Result: {spin_result} ({spin_color}).")
                    print("You lost your bet.")

            elif advanced_choice == 2:  # Six Line
                row_start = int(input("Enter the starting number of the first row (1, 4, 7, ..., 31): "))
                if spin_result in [str(row_start), str(row_start + 1), str(row_start + 2),
                                   str(row_start + 3), str(row_start + 4), str(row_start + 5)]:
                    winnings = bet * 5
                    print(f"The wheel spun... Result: {spin_result} ({spin_color}).")
                    print(f"You guessed correctly! You win ${winnings:.2f}.")
                    player.add_balance(winnings)
                else:
                    print(f"The wheel spun... Result: {spin_result} ({spin_color}).")
                    print("You lost your bet.")
                row_start = int(input("Enter the starting number of the first row (1, 4, 7, ..., 31): "))
                if spin_result in [str(row_start), str(row_start + 1), str(row_start + 2),
                                   str(row_start + 3), str(row_start + 4), str(row_start + 5)]:
                    winnings = bet * 5
                    print(f"The wheel spun... Result: {spin_result} ({spin_color}).")
                    print(f"You guessed correctly! You win ${winnings:.2f}.")
                    player.add_balance(winnings)
                else:
                    print(f"The wheel spun... Result: {spin_result} ({spin_color}).")
                    print("You lost your bet.")

        print("\nOutside Bets:")
        print("1: Red/Black (payout 1:1)")
        print("2: Odd/Even (payout 1:1)")
        print("3: High/Low (payout 1:1)")
        print("4: Dozens (1-12, 13-24, 25-36, payout 2:1)")
        print("5: Columns (first, second, or third, payout 2:1)")

        while True:
            try:
                outside_choice = int(input("Enter your choice (1-5): "))
                if outside_choice in range(1, 6):
                    break
                else:
                    print("Invalid choice. Choose a number between 1 and 5.")
            except ValueError:
                print("Invalid input. Please enter a number between 1 and 5.")
        print("\nOutside Bets:")
        print("1: Red/Black (payout 1:1)")
        print("2: Odd/Even (payout 1:1)")
        print("3: High/Low (payout 1:1)")
        print("4: Dozens (1-12, 13-24, 25-36, payout 2:1)")
        print("5: Columns (first, second, or third, payout 2:1)")

        while True:
            try:
                outside_choice = int(input("Enter your choice (1-5): "))
                if outside_choice in range(1, 6):
                    break
                else:
                    print("Invalid choice. Choose a number between 1 and 5.")
            except ValueError:
                print("Invalid input. Please enter a number between 1 and 5.")

        if outside_choice == 1:  # Red/Black
            while True:
                chosen_color = input("Enter a color (red or black): ").strip().lower()
                if chosen_color in ['red', 'black']:
                    if spin_color == chosen_color:
                        winnings = bet * 2
                        print(f"The wheel spun... Result: {spin_result} ({spin_color}).")
                        print(f"You guessed correctly! You win ${winnings:.2f}.")
                        player.add_balance(winnings)
                    else:
                        print(f"The wheel spun... Result: {spin_result} ({spin_color}).")
                        print("You lost your bet.")
                    break
                else:
            if chosen_color in ['red', 'black']:
                pass
            else:
                print("Invalid color. Please enter 'red' or 'black'.")
            if spin_result in ['0', '00']:
                print("The result was neither odd nor even. You lose.")
            elif (int(spin_result) % 2 != 0 and chosen_odd_even == 'odd'):
                print(f"The wheel spun... Result: {spin_result} ({spin_color}).")
                print(f"You guessed correctly! You win ${winnings:.2f}.")
                player.add_balance(winnings)
            else:
                print(f"The wheel spun... Result: {spin_result} ({spin_color}).")
                print("You lost your bet.")
        elif outside_choice == 3:  # High/Low
            while True:
                chosen_range = input("Enter 'high' (19-36) or 'low' (1-18): ").strip().lower()
                if chosen_range in ['high', 'low']:
                    break
                else:
                    print("Invalid choice. Please enter 'high' or 'low'.")
        elif outside_choice == 4:  # Dozens
            while True:
                try:
                    chosen_dozen = int(input("Enter 1 for 1-12, 2 for 13-24, or 3 for 25-36: "))
                    if chosen_dozen in [1, 2, 3]:
                        break
                    else:
                        print("Invalid choice. Please enter 1, 2, or 3.")
                except ValueError:
                    print("Invalid input. Please enter a number.")
            if spin_result in ['0', '00']:  
                print("The result was not in the chosen range. You lose.")
            elif (chosen_dozen == 1 and 1 <= int(spin_result) <= 12) or \
                 (chosen_dozen == 2 and 13 <= int(spin_result) <= 24) or \
                 (chosen_dozen == 3 and 25 <= int(spin_result) <= 36):
                 (chosen_dozen == 2 and 13 <= int(spin_result) <= 24) or \
                 (chosen_dozen == 3 and 25 <= int(spin_result) <= 36):
                winnings = bet * 3
                print(f"The wheel spun... Result: {spin_result} ({spin_color}).")
                print(f"You guessed correctly! You win ${winnings:.2f}.")
                player.add_balance(winnings)
            else:
                print(f"The wheel spun... Result: {spin_result} ({spin_color}).")
                print("You lost your bet.")
            if spin_result in ['0', '00']:  
                print("The result was not in the chosen range. You lose.")
            elif (chosen_dozen == 1 and 1 <= int(spin_result) <= 12) or \
                 (chosen_dozen == 2 and 13 <= int(spin_result) <= 24) or \
                 (chosen_dozen == 3 and 25 <= int(spin_result) <= 36):
                winnings = bet * 2
                print(f"The wheel spun... Result: {spin_result} ({spin_color}).")
                print(f"You guessed correctly! You win ${winnings:.2f}.")
                player.add_balance(winnings)
            else:
                print(f"The wheel spun... Result: {spin_result} ({spin_color}).")
                print("You lost your bet.")

            if spin_result in ['0', '00']:
                print("The result was not in the chosen range. You lose.")
            elif (1 <= int(spin_result) <= 18 and chosen_range == 'low') or \
                 (19 <= int(spin_result) <= 36 and chosen_range == 'high'):
                winnings = bet * 2
                print(f"The wheel spun... Result: {spin_result} ({spin_color}).")
                print(f"You guessed correctly! You win ${winnings:.2f}.")
                player.add_balance(winnings)
            else:
                print(f"The wheel spun... Result: {spin_result} ({spin_color}).")
                print("You lost your bet.")
            elif (chosen_dozen == 1 and 1 <= int(spin_result) <= 12) or \
                 (chosen_dozen == 2 and 13 <= int(spin_result) <= 24) or \
                 (chosen_dozen == 3 and 25 <= int(spin_result) <= 36):
            winnings = bet * 2
            while True:
                try:
                    chosen_column = int(input("Enter 1 for the first column, 2 for the second, or 3 for the third: "))
                    if chosen_column in [1, 2, 3]:
                        break
                    else:
                        print("Invalid choice. Please enter 1, 2, or 3.")
                except ValueError:
                    print("Invalid input. Please enter a number.")
                print(f"You guessed correctly! You win ${winnings:.2f}.")
                player.add_balance(winnings)
            else:
                print(f"The wheel spun... Result: {spin_result} ({spin_color}).")
                print("You lost your bet.")

        elif outside_choice == 5:  # Columns
            while True:
                try:
                    chosen_column = int(input("Enter 1 for the first column, 2 for the second, or 3 for the third: "))
                    if chosen_column in [1, 2, 3]:
                        break
                    else:
                        print("Invalid choice. Please enter 1, 2, or 3.")
                except ValueError:
                    print("Invalid input. Please enter a number.")
            columns = {
                1: ['1', '4', '7', '10', '13', '16', '19', '22', '25', '28', '31', '34'],
                2: ['2', '5', '8', '11', '14', '17', '20', '23', '26', '29', '32', '35'],
                3: ['3', '6', '9', '12', '15', '18', '21', '24', '27', '30', '33', '36']
            }
            if spin_result in columns[chosen_column]:
                winnings = bet * 2
                print(f"The wheel spun... Result: {spin_result} ({spin_color}).")
                print(f"You guessed correctly! You win ${winnings:.2f}.")
                player.add_balance(winnings)
            else:
                print(f"The wheel spun... Result: {spin_result} ({spin_color}).")
                print("You lost your bet.")