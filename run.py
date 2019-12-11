"""The script file for creating a poker hand analysis file based on cards.py.

This file creates the file analysis.txt to the folder it's run from.
Please see cards.py for further documentation.

"""


from datetime import datetime

from cards import Deck, str_hand_comparison

# Draw cards from a deck and analyse the hands
example_deck = Deck()
poker_hands_list = example_deck.get_list_of_poker_hands(hand_amount=3)
analysis_printable = str_hand_comparison(poker_hands_list)

# Create analysis file
analysis_file = open("analysis.txt", "w+")
analysis_file.write(f"POKER GAME ANALYSIS - {datetime.today().strftime('%Y-%m-%d-%H:%M:%S')}\n")
analysis_file.write("\nThis file contains the analysis of a poker game, played with the following settings:")
analysis_file.write("\n'Three players each receive a random 5-card poker hand picked from a single deck.'\n")
analysis_file.write(analysis_printable)
analysis_file.close()

print("An analysis from a new poker hand simulation was saved in analysis.txt.")