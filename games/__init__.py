# This file makes the games directory a Python package
# Import all games to make them accessible from the games module
import os
import sys

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import all game modules
from games.blackjack import play as blackjack_play
from games.roulette import play as roulette_play
from games.slots import play as slots_play
from games.poker import play as poker_play
from games.baccarat import play as baccarat_play

# Make the play functions available at the module level
blackjack = sys.modules['games.blackjack']
roulette = sys.modules['games.roulette']
slots = sys.modules['games.slots']
poker = sys.modules['games.poker']
baccarat = sys.modules['games.baccarat']