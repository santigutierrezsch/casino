import random
from util import get_valid_bet

def calculate_hand_value(hand):
    value = sum(hand)
    num_aces = hand.count(11)
    while value > 21 and num_aces:
        value -= 10
        num_aces -= 1
    return value

def create_deck():
    deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11] * 4  # 11 represents Ace
    random.shuffle(deck)
    return deck


def play(player):
    print("\n--- Welcome to Blackjack ---")
    print(
        """
        Rules:
        - The goal is to beat the dealer without exceeding 21.
        - Dealer must draw to 17.
        - Blackjack pays 3:2.
        - If the dealer gets 21 (blackjack), the game ends immediately.
        - You can hit as many times as you want, but if you go over 21, you bust.
        """
    )

    bet = get_valid_bet(player.get_balance())
    if bet == 0:  # User wants to exit
        return
    if not player.deduct_balance(bet):
        return

    deck = create_deck()
    player_hand = [deck.pop(), deck.pop()]
    dealer_hand = [deck.pop(), deck.pop()]

    if calculate_hand_value(dealer_hand) == 21:
        print(f"Dealer's hand: {dealer_hand}, Value: 21")
        print("Dealer has blackjack! You lose.")
        print(f"\nYour current balance: ${player.get_balance():.2f}")
        return

    while True:
        print(f"Player's hand: {player_hand}, Value: {calculate_hand_value(player_hand)}")
        print(f"Dealer's hand: [Hidden], {dealer_hand[1]}")

        if calculate_hand_value(player_hand) == 21:
            print("Blackjack! You win!")
            player.add_balance(bet * 2.5)
            print(f"\nYour current balance: ${player.get_balance():.2f}")
            return

        action = input("Do you want to hit or stand? (H/S) ").lower()
        if action == 'h':
            player_hand.append(deck.pop())
            if calculate_hand_value(player_hand) > 21:
                print(f"Player's hand: {player_hand}, Value: {calculate_hand_value(player_hand)}")
                print("Bust! You lose.")
                print(f"\nYour current balance: ${player.get_balance():.2f}")
                return
        elif action == 's':
            break
        else:
            print("Invalid input. Please choose 'H' to hit or 'S' to stand.")

    while calculate_hand_value(dealer_hand) < 17:
        dealer_hand.append(deck.pop())

    print(f"Dealer's hand: {dealer_hand}, Value: {calculate_hand_value(dealer_hand)}")
    player_value = calculate_hand_value(player_hand)
    dealer_value = calculate_hand_value(dealer_hand)

    if dealer_value > 21 or player_value > dealer_value:
        print("You win!")
        player.add_balance(bet * 2)
    elif player_value < dealer_value:
        print("You lose.")
    else:
        print("It's a tie!")
        player.add_balance(bet)
    
    print(f"\nYour current balance: ${player.get_balance():.2f}")