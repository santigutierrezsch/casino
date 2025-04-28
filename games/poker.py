import random
import time
from util import get_valid_bet, clear_screen
from player import Player
from collections import Counter

class Bot(Player):
    def __init__(self, balance, personality="Aggressive"):
        if not hasattr(Bot, 'counter'):
            Bot.counter = 1
        else:
            Bot.counter += 1
        super().__init__(balance, name=f"Bot {Bot.counter}")
        self.personality = personality

    def choose_action(self, pot, current_bet, hand_strength=0):
        # Factor in hand strength for more realistic bot behavior
        # Hand strength is on a scale of 0-9 where 9 is a royal flush
        strength_factor = 1 + (hand_strength / 5)  # Creates a multiplier from 1.0 to 2.8
        
        if self.personality == "Aggressive":
            # Check if we have enough balance to raise
            if current_bet + 10 <= self.balance:
                # More likely to raise with better hands
                if random.random() < 0.7 * strength_factor:
                    return "raise", random.randint(current_bet + 10, min(self.balance, pot // 2))
                elif current_bet <= self.balance:
                    return "call", current_bet
                else:
                    return "fold", 0
            elif current_bet <= self.balance:
                return "call", current_bet
            else:
                return "fold", 0
        elif self.personality == "Cautious":
            # Only calls with decent hands, otherwise folds
            if hand_strength >= 1 and current_bet <= self.balance:
                return "call", current_bet
            else:
                return "fold", 0
        elif self.personality == "Bluffer":
            # Occasionally raises with weak hands
            actions = []
            if current_bet < self.balance:
                bluff_chance = 0.3
                if hand_strength <= 2:
                    bluff_chance = 0.5  # More likely to bluff with weak hands
                
                if random.random() < bluff_chance:
                    actions.append(("raise", random.randint(current_bet, min(self.balance, pot // 3))))
            
            if current_bet <= self.balance:
                actions.append(("call", current_bet))
            
            actions.append(("fold", 0))
            return random.choice(actions)
        elif self.personality == "Passive":
            # Almost always calls if possible
            return ("call", current_bet) if current_bet <= self.balance else ("fold", 0)
        elif self.personality == "Optimist":
            # Always believes their hand is good
            if current_bet < self.balance:
                if hand_strength >= 3 or random.random() < 0.3:
                    return "raise", random.randint(current_bet, min(max(current_bet + 10, pot // 4), self.balance))
                else:
                    return "call", current_bet
            elif current_bet <= self.balance:
                return "call", current_bet
            else:
                return "fold", 0
        elif self.personality == "Strategist":
            # Makes calculated bets based on hand strength
            if hand_strength >= 4 and current_bet * 2 <= self.balance:
                return "raise", current_bet * 2
            elif hand_strength >= 1 and current_bet <= self.balance:
                return "call", current_bet
            else:
                return "fold", 0
        elif self.personality == "Risky":
            # Takes big risks with decent hands
            if hand_strength >= 2 and current_bet * 2 <= self.balance:
                return "raise", random.randint(current_bet * 2, min(self.balance, pot // 2))
            elif current_bet <= self.balance:
                return "call", current_bet
            else:
                return "fold", 0
        elif self.personality == "Loyal":
            # Almost always stays in the game
            return ("call", current_bet) if current_bet <= self.balance else ("fold", 0)
        elif self.personality == "Calculating":
            # Only plays with good odds
            if hand_strength > 2:
                return ("call", current_bet) if current_bet <= self.balance else ("fold", 0)
            else:
                return ("fold", 0)
        elif self.personality == "Defender":
            # Conservative with money
            return ("fold", 0) if current_bet > self.balance // 2 or hand_strength < 1 else ("call", current_bet)
        else:
            return ("call", current_bet) if current_bet <= self.balance else ("fold", 0)


def create_deck():
    suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
    ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]
    return [(rank, suit) for rank in ranks for suit in suits]


def deal_hands(deck, players):
    hands = {}
    for p in players:
        hands[p.name] = [deck.pop(), deck.pop()]
    return hands


def get_rank_value(rank):
    """Convert card rank to numeric value"""
    rank_values = {
        "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10,
        "Jack": 11, "Queen": 12, "King": 13, "Ace": 14
    }
    return rank_values.get(rank, 0)


def evaluate_hand(hand, community_cards):
    """
    Evaluate a poker hand (2 hole cards + community cards).
    Returns a tuple with (hand_rank, tiebreaker_values)
    Hand ranks are:
    9: Royal Flush
    8: Straight Flush
    7: Four of a Kind
    6: Full House
    5: Flush
    4: Straight
    3: Three of a Kind
    2: Two Pair
    1: One Pair
    0: High Card
    """
    # Combine hole cards and community cards
    all_cards = hand + community_cards
    
    # Extract ranks and suits
    ranks = [card[0] for card in all_cards]
    suits = [card[1] for card in all_cards]
    
    # Convert ranks to values
    rank_values = [get_rank_value(rank) for rank in ranks]
    rank_values.sort(reverse=True)  # Sort in descending order
    
    # Count occurrences of each rank and suit
    rank_counts = Counter(rank_values)
    suit_counts = Counter(suits)
    
    # Check for flush
    is_flush = any(count >= 5 for count in suit_counts.values())
    if is_flush:
        flush_suit = max(suit_counts.items(), key=lambda x: x[1])[0]
        flush_cards = [get_rank_value(card[0]) for card in all_cards if card[1] == flush_suit]
        flush_cards.sort(reverse=True)
        flush_values = flush_cards[:5]  # Top 5 cards of the flush
    
    # Check for straight
    unique_values = sorted(set(rank_values), reverse=True)
    straight_values = []
    
    # Handle Ace as low card for A-5-4-3-2 straight
    if 14 in unique_values and all(val in unique_values for val in [2, 3, 4, 5]):
        straight_values = [5, 4, 3, 2, 1]  # Ace counts as 1 in this case
    
    if not straight_values:
        for i in range(len(unique_values) - 4):
            if unique_values[i] - unique_values[i + 4] == 4:
                straight_values = unique_values[i:i + 5]
                break
    
    is_straight = len(straight_values) >= 5
    
    # Royal Flush
    if is_flush and is_straight and straight_values[0] == 14:
        return (9, [14])
    
    # Straight Flush
    if is_flush and is_straight:
        return (8, straight_values)
    
    # Four of a Kind
    four_kind = [rank for rank, count in rank_counts.items() if count == 4]
    if four_kind:
        kickers = [r for r in rank_values if r != four_kind[0]][:1]
        return (7, four_kind + kickers)
    
    # Full House
    three_kind = [rank for rank, count in rank_counts.items() if count == 3]
    pairs = [rank for rank, count in rank_counts.items() if count == 2]
    
    if three_kind and pairs:
        return (6, [max(three_kind), max(pairs)])
    elif len(three_kind) >= 2:
        three_kind.sort(reverse=True)
        return (6, three_kind[:2])
    
    # Flush
    if is_flush:
        return (5, flush_values)
    
    # Straight
    if is_straight:
        return (4, straight_values)
    
    # Three of a Kind
    if three_kind:
        kickers = [r for r in rank_values if r != three_kind[0]][:2]
        return (3, [three_kind[0]] + kickers)
    
    # Two Pair
    if len(pairs) >= 2:
        pairs.sort(reverse=True)
        kickers = [r for r in rank_values if r not in pairs[:2]][:1]
        return (2, pairs[:2] + kickers)
    
    # One Pair
    if pairs:
        kickers = [r for r in rank_values if r != pairs[0]][:3]
        return (1, [pairs[0]] + kickers)
    
    # High Card
    return (0, rank_values[:5])


def get_hand_name(hand_rank):
    """Convert hand rank to string description"""
    hand_names = {
        9: "Royal Flush",
        8: "Straight Flush",
        7: "Four of a Kind",
        6: "Full House",
        5: "Flush",
        4: "Straight",
        3: "Three of a Kind",
        2: "Two Pair",
        1: "Pair",
        0: "High Card"
    }
    return hand_names.get(hand_rank, "Unknown")


def display_hand(player_name, hand, highlight=False):
    """Display a player's hand with optional highlighting"""
    suit_symbols = {
        "Hearts": "♥",
        "Diamonds": "♦",
        "Clubs": "♣",
        "Spades": "♠"
    }
    
    card1 = f"{hand[0][0]} of {hand[0][1]} {suit_symbols.get(hand[0][1], '')}"
    card2 = f"{hand[1][0]} of {hand[1][1]} {suit_symbols.get(hand[1][1], '')}"
    
    if highlight:
        print(f"\033[1m{player_name}'s hand: {card1}, {card2}\033[0m")
    else:
        print(f"{player_name}'s hand: {card1}, {card2}")
    
    time.sleep(0.5)


def display_community_cards(community_cards):
    """Display community cards with suit symbols"""
    suit_symbols = {
        "Hearts": "♥",
        "Diamonds": "♦",
        "Clubs": "♣",
        "Spades": "♠"
    }
    
    card_texts = []
    for rank, suit in community_cards:
        symbol = suit_symbols.get(suit, '')
        card_texts.append(f"{rank} of {suit} {symbol}")
    
    print(f"Community Cards: {', '.join(card_texts)}")
    time.sleep(1)


def show_bot_thinking(bot_name, personality, hand, community_cards):
    """Show what the bot might be thinking based on personality and hand"""
    # Simplistic hand strength assessment
    if not community_cards:
        # Pre-flop
        high_card = max(get_rank_value(hand[0][0]), get_rank_value(hand[1][0]))
        is_pair = hand[0][0] == hand[1][0]
        is_suited = hand[0][1] == hand[1][1]
        
        if is_pair:
            think = "looks at pair with interest"
            if get_rank_value(hand[0][0]) > 10:
                think = "seems excited about high pair"
        elif high_card > 12:
            think = "considers high card strength"
        elif is_suited:
            think = "contemplates suited cards"
        else:
            think = "examines cards carefully"
    else:
        # Post-flop
        hand_value = evaluate_hand(hand, community_cards)
        hand_rank = hand_value[0]
        
        if hand_rank >= 6:  # Full house or better
            think = "trying to hide excitement"
        elif hand_rank >= 3:  # Three of a kind or better
            think = "seems confident"
        elif hand_rank >= 1:  # Pair
            think = "looks thoughtful"
        else:
            think = "keeps a poker face"
    
    # Personality modifiers
    if personality == "Bluffer":
        print(f"{bot_name} ({personality}) {think}, but expression is unreadable")
    elif personality == "Aggressive":
        print(f"{bot_name} ({personality}) {think} and seems eager to bet")
    elif personality == "Cautious":
        print(f"{bot_name} ({personality}) {think} with a measured expression")
    elif personality == "Optimist":
        print(f"{bot_name} ({personality}) {think} with a smile")
    else:
        print(f"{bot_name} ({personality}) {think}")
        
    time.sleep(0.8)


def play(player):
    clear_screen()
    print("\n--- Welcome to Poker ---")
    bet = get_valid_bet(player.get_balance())
    if bet == 0:  # User wants to exit
        return
    if not player.deduct_balance(bet):
        return

    deck = create_deck()
    random.shuffle(deck)

    print("Choose your poker game:")
    print("1. Five Card Draw (single player)")
    print("2. Texas Hold'em (with bots)")
    choice = input("Enter your choice (1 or 2): ").strip()

    if choice == "1":
        # Five Card Draw - Single player mode
        player_hand = [deck.pop() for _ in range(5)]
        print("\nYour initial hand:")
        for i, card in enumerate(player_hand):
            print(f"{i+1}. {card[0]} of {card[1]}")
            
        # Allow player to discard and replace cards
        print("\nYou can discard up to 3 cards and replace them")
        discard = input("Enter the numbers of cards to discard (e.g., '1 3 5') or press Enter to keep all: ").strip()
        
        if discard:
            try:
                discard_indices = [int(i) - 1 for i in discard.split()]
                if 0 <= len(discard_indices) <= 3:
                    for idx in sorted(discard_indices, reverse=True):
                        if 0 <= idx < len(player_hand):
                            print(f"Discarded: {player_hand[idx][0]} of {player_hand[idx][1]}")
                            player_hand[idx] = deck.pop()
                else:
                    print("You can only discard up to 3 cards. No cards were replaced.")
            except:
                print("Invalid input. No cards were replaced.")
        
        print("\nYour final hand:")
        for i, card in enumerate(player_hand):
            print(f"{i+1}. {card[0]} of {card[1]}")
            
        # Evaluate hand
        hand_rank, _ = evaluate_hand(player_hand[:2], player_hand[2:])
        hand_name = get_hand_name(hand_rank)
        print(f"\nYou have a {hand_name}!")
        
        # Determine payout based on hand rank
        payouts = {
            0: 0,    # High card
            1: 1,    # One pair
            2: 2,    # Two pair
            3: 3,    # Three of a kind
            4: 5,    # Straight
            5: 7,    # Flush
            6: 10,   # Full house
            7: 20,   # Four of a kind
            8: 50,   # Straight flush
            9: 100   # Royal flush
        }
        
        multiplier = payouts.get(hand_rank, 0)
        if multiplier > 0:
            winnings = bet * multiplier
            print(f"You win ${winnings:.2f}! ({multiplier}x your bet)")
            player.add_balance(winnings)
        else:
            print("Sorry, you need at least a pair to win. You lost your bet.")
        
        print(f"\nYour current balance: ${player.get_balance():.2f}")

    elif choice == "2":
        # Texas Hold'em with bots
        num_bots = 3
        bot_personalities = [
            "Aggressive", "Cautious", "Bluffer", "Passive", "Optimist", 
            "Strategist", "Risky", "Loyal", "Calculating", "Defender"
        ]
        bots = [Bot(1000, random.choice(bot_personalities)) for _ in range(num_bots)]
        
        # Show bot personalities
        print("\nYou're playing against:")
        for bot in bots:
            print(f"- {bot.name} ({bot.personality}) with ${bot.get_balance():.2f}")
            
        players = [player] + bots
        hands = deal_hands(deck, players)
        community_cards = []

        pot = bet
        current_bet = bet
        
        # Display player's cards with a highlight
        print("\nYour cards:")
        display_hand(player.name, hands[player.name], highlight=True)

        for round_num in range(4):
            print(f"\n--- Betting Round {round_num + 1} ---")

            if round_num == 0:
                print("\n--- Pre-Flop ---")
                # Show bots "thinking" based on their cards
                for bot in bots:
                    if bot in players:
                        show_bot_thinking(bot.name, bot.personality, hands[bot.name], [])

            elif round_num == 1:
                print("\nDealing the Flop (3 cards)...")
                community_cards.extend([deck.pop() for _ in range(3)])
                display_community_cards(community_cards)
                
                # Show current hand evaluation
                player_hand_rank, _ = evaluate_hand(hands[player.name], community_cards)
                print(f"Your current hand: {get_hand_name(player_hand_rank)}")
                
                # Show bots "thinking" with updated information
                for bot in bots:
                    if bot in players:
                        show_bot_thinking(bot.name, bot.personality, hands[bot.name], community_cards)

            elif round_num == 2:
                print("\nDealing the Turn (1 card)...")
                community_cards.append(deck.pop())
                display_community_cards(community_cards)
                
                # Show current hand evaluation
                player_hand_rank, _ = evaluate_hand(hands[player.name], community_cards)
                print(f"Your current hand: {get_hand_name(player_hand_rank)}")
                
                # Show bots "thinking" with updated information
                for bot in bots:
                    if bot in players:
                        show_bot_thinking(bot.name, bot.personality, hands[bot.name], community_cards)

            elif round_num == 3:
                print("\nDealing the River (1 card)...")
                community_cards.append(deck.pop())
                display_community_cards(community_cards)
                
                # Show current hand evaluation
                player_hand_rank, _ = evaluate_hand(hands[player.name], community_cards)
                print(f"Your current hand: {get_hand_name(player_hand_rank)}")
                
                # Show bots "thinking" with updated information
                for bot in bots:
                    if bot in players:
                        show_bot_thinking(bot.name, bot.personality, hands[bot.name], community_cards)

            # Player's turn first
            if player in players:
                print(f"\n--- Your Turn ---")
                print(f"Current bet: ${current_bet:.2f}")
                print(f"Your balance: ${player.get_balance():.2f}")
                print(f"Pot size: ${pot:.2f}")
                
                valid_actions = ["fold"]
                if current_bet <= player.get_balance():
                    valid_actions.append("call")
                if player.get_balance() > current_bet:
                    valid_actions.append("raise")
                
                # Add check option if no betting has occurred
                if current_bet == 0:
                    valid_actions.append("check")
                
                action = None
                while action not in valid_actions:
                    action_prompt = "/".join(valid_actions)
                    action = input(f"Choose action ({action_prompt}): ").lower().strip()
                    if action not in valid_actions:
                        print(f"Invalid action. Choose from: {', '.join(valid_actions)}")
                
                if action == "fold":
                    print(f"{player.name} folds.")
                    players.remove(player)
                elif action == "call":
                    amount = min(current_bet, player.get_balance())
                    if player.deduct_balance(amount):
                        print(f"{player.name} calls with ${amount:.2f}.")
                        pot += amount
                    else:
                        print(f"{player.name} cannot call due to insufficient balance.")
                        players.remove(player)
                elif action == "check":
                    print(f"{player.name} checks.")
                elif action == "raise":
                    max_raise = player.get_balance()
                    raise_amount = None
                    while raise_amount is None or raise_amount <= current_bet or raise_amount > max_raise:
                        try:
                            raise_prompt = f"Enter raise amount (more than ${current_bet:.2f}, max ${max_raise:.2f}): "
                            raise_amount = float(input(raise_prompt))
                            if raise_amount <= current_bet:
                                print(f"Raise amount must be more than the current bet (${current_bet:.2f}).")
                            elif raise_amount > max_raise:
                                print(f"You don't have enough balance for that raise. Maximum: ${max_raise:.2f}")
                        except ValueError:
                            print("Please enter a valid number.")
                    
                    if player.deduct_balance(raise_amount):
                        print(f"{player.name} raises to ${raise_amount:.2f}.")
                        current_bet = raise_amount
                        pot += raise_amount
                    else:
                        print(f"{player.name} cannot raise due to insufficient balance.")
                        players.remove(player)

            # Bot betting loop
            remaining_bots = [bot for bot in bots if bot in players]
            for bot in remaining_bots:
                # Evaluate bot's hand to inform decision
                bot_hand_strength = 0
                if community_cards:
                    bot_hand_value, _ = evaluate_hand(hands[bot.name], community_cards)
                    bot_hand_strength = bot_hand_value[0]
                
                action, amount = bot.choose_action(pot, current_bet, bot_hand_strength)

                if action == "fold":
                    print(f"{bot.name} folds.")
                    # Show what they folded for interest
                    if random.random() < 0.5:  # Sometimes show folded cards
                        display_hand(f"{bot.name} (folded)", hands[bot.name])
                    players.remove(bot)
                elif action == "call":
                    amount = min(current_bet, bot.get_balance())
                    if bot.deduct_balance(amount):
                        print(f"{bot.name} calls with ${amount:.2f}.")
                        pot += amount
                    else:
                        print(f"{bot.name} cannot call due to insufficient balance.")
                        players.remove(bot)
                elif action == "raise":
                    if bot.get_balance() >= amount:
                        if bot.deduct_balance(amount):
                            print(f"{bot.name} raises to ${amount:.2f}.")
                            current_bet = amount
                            pot += amount
                        else:
                            print(f"{bot.name} cannot raise due to insufficient balance.")
                            players.remove(bot)
                    else:
                        print(f"{bot.name} wanted to raise to ${amount:.2f} but doesn't have enough.")
                        if bot.get_balance() >= current_bet:
                            if bot.deduct_balance(current_bet):
                                print(f"{bot.name} calls instead with ${current_bet:.2f}.")
                                pot += current_bet
                            else:
                                print(f"{bot.name} folds due to insufficient balance.")
                                players.remove(bot)
                        else:
                            print(f"{bot.name} folds due to insufficient balance.")
                            players.remove(bot)

            # If all but one player has folded, end the game
            if len(players) <= 1:
                break

        print("\n--- Final Results ---")
        print("\nCommunity Cards:")
        if community_cards:
            display_community_cards(community_cards)
        
        # Show all hands (including folded players for interest)
        print("\nAll Hands:")
        for p_name, p_hand in hands.items():
            is_active = any(p.name == p_name for p in players)
            display_hand(f"{p_name}{' (active)' if is_active else ' (folded)'}", p_hand)

        print(f"\nFinal pot: ${pot:.2f}")
        
        if len(players) == 0:
            print("All players folded! The house takes the pot.")
        elif len(players) == 1:
            winner = players[0]
            print(f"{winner.name} wins the pot of ${pot:.2f}!")
            winner.add_balance(pot)
        else:
            # Evaluate hands for each player
            player_hands = {}
            for p in players:
                hand_value = evaluate_hand(hands[p.name], community_cards)
                player_hands[p.name] = hand_value
                hand_name = get_hand_name(hand_value[0])
                print(f"{p.name} has a {hand_name}")
            
            # Find the winner(s)
            best_hand = max(player_hands.values())
            winners = [p for p, hand in player_hands.items() if hand == best_hand]
            
            if len(winners) == 1:
                winner_name = winners[0]
                winner = next(p for p in players if p.name == winner_name)
                print(f"{winner_name} wins with a {get_hand_name(best_hand[0])}!")
                winner.add_balance(pot)
            else:
                # Split pot for ties
                split_amount = pot / len(winners)
                print(f"Tie! The pot is split among {', '.join(winners)}.")
                for p in players:
                    if p.name in winners:
                        print(f"{p.name} receives ${split_amount:.2f}")
                        p.add_balance(split_amount)

        print(f"\nYour current balance: ${player.get_balance():.2f}")

    else:
        print("Invalid choice.")