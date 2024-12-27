import random
from util import get_valid_bet

def play(player):
    print("\n--- Welcome to Baccarat ---")
    print("In Baccarat, you can bet on:")
    print("1: Player (payout 1:1)")
    print("2: Banker (payout 1:1)")
    print("3: Tie (payout 8:1)")

    bet = get_valid_bet(player.get_balance())
    if not player.deduct_balance(bet):
        return

    while True:
        try:
            bet_type = int(input("Enter your bet (1 for Player, 2 for Banker, 3 for Tie): "))
            if bet_type not in [1, 2, 3]:
                print("Invalid choice. Choose 1, 2, or 3.")
            else:
                break
        except ValueError:
            print("Invalid input. Please enter 1, 2, or 3.")

    def draw_card():
        return random.randint(1, 13) % 10

    def calculate_score(hand):
        return sum(hand) % 10

    player_hand = [draw_card(), draw_card()]
    banker_hand = [draw_card(), draw_card()]

    player_score = calculate_score(player_hand)
    banker_score = calculate_score(banker_hand)

    print(f"\nPlayer's hand: {player_hand}, score: {player_score}")
    print(f"Banker's hand: {banker_hand}, score: {banker_score}")

    if player_score < 8 and banker_score < 8:
        if player_score <= 5:
            player_hand.append(draw_card())
            player_score = calculate_score(player_hand)
            print(f"Player draws a card: {player_hand[-1]}, new score: {player_score}")

        if banker_score <= 5:
            if len(player_hand) == 3:
                third_card = player_hand[2]
                if banker_score < 3 or \
                   (banker_score == 3 and third_card != 8) or \
                   (banker_score == 4 and third_card in [2, 3, 4, 5, 6, 7]) or \
                   (banker_score == 5 and third_card in [4, 5, 6, 7]) or \
                   (banker_score == 6 and third_card in [6, 7]):
                    banker_hand.append(draw_card())
                    banker_score = calculate_score(banker_hand)
                    print(f"Banker draws a card: {banker_hand[-1]}, new score: {banker_score}")
            elif banker_score <= 5:
                banker_hand.append(draw_card())
                banker_score = calculate_score(banker_hand)
                print(f"Banker draws a card: {banker_hand[-1]}, new score: {banker_score}")

    print(f"\nFinal Scores: Player {player_score}, Banker {banker_score}")

    if player_score > banker_score:
        print("Player wins!")
        if bet_type == 1:
            winnings = bet * 2
            print(f"You bet on Player and win ${winnings - bet:.2f}.")
            player.add_balance(winnings)
        else:
            print("You lost your bet.")
    elif banker_score > player_score:
        print("Banker wins!")
        if bet_type == 2:
            winnings = bet * 2
            print(f"You bet on Banker and win ${winnings - bet:.2f}.")
            player.add_balance(winnings)
        else:
            print("You lost your bet.")
    else:
        print("It's a tie!")
        if bet_type == 3:
            winnings = bet * 9
            print(f"You bet on Tie and win ${winnings - bet:.2f}.")
            player.add_balance(winnings)
        else:
            print("You lost your bet.")