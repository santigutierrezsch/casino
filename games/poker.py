import random
import time
from util import get_valid_bet, clear_screen
from player import Player

class Bot(Player):
    def __init__(self, balance, personality="Aggressive"):
        if not hasattr(Bot, 'counter'):
            Bot.counter = 1
        else:
            Bot.counter += 1
        super().__init__(balance, name=f"Bot {Bot.counter}")
        self.personality = personality

    def choose_action(self, pot, current_bet):
        if self.personality == "Aggressive":
            return "raise", random.randint(current_bet + 10, min(self.balance, pot // 2))
        elif self.personality == "Cautious":
            return ("call", current_bet) if current_bet <= self.balance else ("fold", 0)
        elif self.personality == "Bluffer":
            return random.choice([("raise", random.randint(current_bet, pot // 4)), ("call", current_bet), ("fold", 0)])
        elif self.personality == "Passive":
            return ("call", current_bet) if current_bet <= self.balance else ("fold", 0)
        elif self.personality == "Optimist":
            return "raise", random.randint(current_bet, min(max(current_bet + 10, pot // 4), self.balance))
        elif self.personality == "Strategist":
            return "raise", current_bet * 2
        elif self.personality == "Risky":
            return "raise", random.randint(current_bet * 2, min(self.balance, pot // 2))
        elif self.personality == "Loyal":
            return "call", current_bet
        elif self.personality == "Calculating":
            return ("fold", 0) if current_bet * 2 > self.balance else ("call", current_bet)
        elif self.personality == "Defender":
            return ("fold", 0) if current_bet > self.balance else ("call", current_bet)
        else:
            return "call", current_bet



def create_deck():
    suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
    ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]
    return [(rank, suit) for rank in ranks for suit in suits]


def deal_hands(deck, players):
    hands = {}
    for p in players:
        hands[p.name] = [deck.pop(), deck.pop()]
    return hands


def evaluate_hand(hand):
    """Simulated hand evaluation (can be replaced with actual poker rules)."""
    return random.choice(["High Card", "Pair", "Flush", "Straight"])


def display_hand(player_name, hand):
    print(f"{player_name}'s hand: {hand[0]}, {hand[1]}")
    time.sleep(1)


def display_community_cards(community_cards):
    print(f"Community Cards: {', '.join([f'{rank} of {suit}' for rank, suit in community_cards])}")
    time.sleep(1)


def play(player):
    clear_screen()
    print("\n--- Welcome to Poker ---")
    bet = get_valid_bet(player.get_balance())
    if not player.deduct_balance(bet):
        return

    deck = create_deck()
    random.shuffle(deck)

    print("Choose your poker game:")
    print("1. Regular Poker")
    print("2. Texas Hold'em (with bots)")
    choice = input("Enter your choice (1 or 2): ").strip()

    if choice == "1":
        player_hand = [deck.pop(), deck.pop()]
        print(f"Your hand: {player_hand[0]}, {player_hand[1]}")
        result = evaluate_hand(player_hand)
        print(f"You got a {result}!")
        winnings = bet * random.choice([0, 2])
        if winnings > 0:
            print(f"You win ${winnings:.2f}!")
            player.add_balance(winnings)
        else:
            print("You lost your bet.")

    elif choice == "2":
        num_bots = 3
        bot_personalities = [
            "Aggressive", "Cautious", "Bluffer", "Passive", "Optimist", 
            "Strategist", "Risky", "Loyal", "Calculating", "Defender"
        ]
        bots = [Bot(1000, random.choice(bot_personalities)) for _ in range(num_bots)]
        players = [player] + bots

        hands = deal_hands(deck, players)
        community_cards = []

        pot = bet
        current_bet = bet
        for round_num in range(4):
            print(f"\n--- Betting Round {round_num + 1} ---")

            if round_num == 0:
                print("\n--- Pre-Flop ---")
                time.sleep(1)
                for p in players:
                    display_hand(p.name, hands[p.name])
                time.sleep(1)

            elif round_num == 1:
                print("\nDealing the Flop (3 cards)...")
                community_cards.extend([deck.pop() for _ in range(3)])
                display_community_cards(community_cards)

            elif round_num == 2:
                print("\nDealing the Turn (1 card)...")
                community_cards.append(deck.pop())
                display_community_cards(community_cards)

            elif round_num == 3:
                print("\nDealing the River (1 card)...")
                community_cards.append(deck.pop())
                display_community_cards(community_cards)

            # Player betting loop
            for p in players[:]:
                action, amount = p.choose_action(pot, current_bet)

                if action == "raise":
                    print(f"{p.name} raises by ${amount}.")
                    if p.deduct_balance(amount):
                        current_bet = amount
                    if p.deduct_balance(amount):
                        print(f"{p.name} raises by ${amount}.")
                    if p.deduct_balance(current_bet):
                        print(f"{p.name} calls.")
                        pot += current_bet
                    else:
                        print(f"{p.name} cannot call due to insufficient balance.")
                        print(f"{p.name} tried to raise by ${amount} but didn't have enough balance.")
                        pot += current_bet
                elif action == "fold":
                    print(f"{p.name} folds.")
                    players.remove(p)

        print("\n--- Final Results ---")
        for p in players:
            display_hand(p.name, hands[p.name])

        print(f"Final pot: ${pot}")
        winner = random.choice(players)
        print(f"{winner.name} wins the pot of ${pot}!")
        winner.add_balance(pot)

    else:
        print("Invalid choice.")