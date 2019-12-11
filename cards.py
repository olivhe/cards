"""Tools for drawing cards, comparing poker hands and reporting the results.

The module was created to make random draws from a card deck and analyse the
results. Any number of cards or hands can be drawn from a simulated deck and
the results then analysed - both the hand and a number of hands.

The results can be printed to a longer string for reporting using the
str_hand_comparison function.

The program includes a number simple tests. These only cover a part of the
card handling and hand ordering functions' outputs, and are likely to prove
useful only in case of further development.


  Typical usage example:

  example_deck = Deck()
  poker_hands_list = example_deck.get_list_of_poker_hands(hand_amount=3)
  print(str_hand_comparison(poker_hands_list))

"""


import random
import copy

import inflect


def num_conv(number, plural=False):
    """Converts card numbers into their proper names

    Args:
        number (int): The number intended to be converted
        plural (bool): Determines if the result should be in plural or single form

    Returns:
        The proper name to be used for the card number

    """
    if plural:
        plural_s = "s"
    else:
        plural_s = ""

    if number == 1 or number == 14:
        number_string = f"Ace{plural_s}"
    elif number == 11:
        number_string = f"Jack{plural_s}"
    elif number == 12:
        number_string = f"Queen{plural_s}"
    elif number == 13:
        number_string = f"King{plural_s}"
    else:
        number_string = f"{str(number)}{plural_s}"
    return number_string


def order_hands(hand_list):
    """Returns the best hand from a list of PokerHands with the index of the determining high card

    Args:
        hand_list (list): A list of PokerHand objects to analyze

    Returns:
        winning_hand (PokerHand): The best PokerHand given in hand_list
        kicker_index (int): The index of the kicker used to determine the best hand; often 0

    """
    def sort_by_high_cards(hands_to_sort):
        # Assume high cards to be in order from highest to lowest points
        def sort_term(hand):
            sort_list = []
            for kicker_card in hand.kickers:
                sort_list.append(kicker_card.points)
            return tuple(sort_list)
        kickers_sorted = sorted(hands_to_sort, key=lambda hand: sort_term(hand), reverse=True)
        determining_kicker_index = -1  # Stays -1 if it's a draw
        for card_index, kicker in enumerate(kickers_sorted[0].kickers):
            if kickers_sorted[1].kickers[card_index].points != kicker.points:
                determining_kicker_index = card_index + 1
                break
        return kickers_sorted, determining_kicker_index

    kicker_index = -2  # Stays -2 unless high cards are needed to make a difference
    # First sort and filter the list to contain only the highest hand scores on the list
    sorted_hands = sorted(hand_list, key=lambda x: x.score[0], reverse=True)
    highest_hands = [x for x in sorted_hands if x.score[0] == sorted_hands[0].score[0]]
    # Depending on the type of the secondary compare term order the cards with the best primary hand scores
    if isinstance(highest_hands[0].score[1], tuple):
        sorted_high_hands = sorted(highest_hands, key=lambda x: (x.score[1][0], x.score[1][1]), reverse=True)
        if len(sorted_high_hands) > 1:
            if sorted_high_hands[0].score[1][0] == sorted_high_hands[1].score[1][0]:
                if sorted_high_hands[0].score[1][1] == sorted_high_hands[1].score[1][1]:
                    # The secondary scoring was the same, so we check the kickers.
                    # Kickers can only score with flushes, threes of a kind, pairs, and two pairs
                    filtered_hands = list(filter(lambda x: (x.score[1][0] == sorted_high_hands[0].score[1][0],
                                                            x.score[1][1] == sorted_high_hands[0].score[1][1]),
                                                 sorted_high_hands))
                    sorted_high_hands, kicker_index = sort_by_high_cards(filtered_hands)
    else:  # Expects int
        sorted_high_hands = sorted(highest_hands, key=lambda x: x.score[1], reverse=True)
        if len(sorted_high_hands) > 1:
            if sorted_high_hands[0].score[1] == sorted_high_hands[1].score[1]:
                # The secondary scoring was the same, so we check the kickers.
                # Kickers can only score with flushes, threes of a kind, pairs, and two pairs
                filtered_hands = [x for x in sorted_high_hands if x.score[1] == sorted_high_hands[0].score[1]]
                sorted_high_hands, kicker_index = sort_by_high_cards(filtered_hands)
    # The last thing we need to check is if it's a draw.
    if len(sorted_high_hands) > 1:
        if sorted_high_hands[0]:
            pass
    winning_hand = sorted_high_hands[0]
    return winning_hand, kicker_index


def str_hand_comparison(poker_hands):
    """Compares the poker hands and describes the results

    The string includes info on the winning hand, possibles draws and the cards of each hand.
    High cards making a difference in the comparison are marked with "(high card".
    The cards not contributing or effecting the win are enclosed in brackets.

    Args:
        poker_hands (list): A list of PokerHand objects to be compared

    Returns:
        A multiline string with a comparison of the poker hands, e.g.:

            -<>-<>-<>-<>-<>-<>-<>-<>-
            The first hand wins with a Royal Flush.
            -<>-<>-<>-<>-<>-<>-<>-<>-
            1st hand: Royal Flush
            Winning hand
            The hand includes the following cards:
             - Ace of clubs
             - King of clubs
             - Queen of clubs
             - Jack of clubs
             - 10 of clubs
            -<>-<>-<>-<>-<>-<>-<>-<>-
            2nd hand: Straight Flush, 9 to King
            ...

    Raises:
        ValueError: The kicker_det signifies a draw, but no equal hands to the best hand were found
        ValueError: The kicker_det signifies a difference by kickers, but found no equal primary hand

        kicker_det is defined by order_hands(poker_hands)

    """
    best_hand, kicker_det = order_hands(poker_hands)
    p = inflect.engine()
    best_index = None
    best_indices = []
    # List the indices of the winning hands and form the win statement
    if kicker_det != -1:  # One winner
        for hand_index, poker_hand in enumerate(poker_hands):
            if poker_hand.description == best_hand.description:
                if kicker_det > -1:
                    kicker_points = [kicker.points for kicker in poker_hand.kickers]
                    for best_kicker in best_hand.kickers:
                        if best_kicker.points in kicker_points:
                            kicker_points.pop(kicker_points.index(best_kicker.points))
                    if len(kicker_points) == 0:
                        best_index = hand_index
                    else:
                        pass
                else:
                    best_index = hand_index
        win_statement = f"The {p.number_to_words(p.ordinal(best_index+1))} hand wins with {str(best_hand)}."
    else:
        # It's a draw, so we need to know how which hands are the same
        for hand_index, poker_hand in enumerate(poker_hands):
            if poker_hand.description == best_hand.description:
                kicker_points = [high_card.points for high_card in poker_hand.kickers]
                for best_kicker in best_hand.kickers:
                    if best_kicker.points in kicker_points:
                        kicker_points.pop(kicker_points.index(best_kicker.points))
                if len(kicker_points) == 0:
                    best_indices.append(hand_index)
                else:
                    pass
        if len(best_indices) < 2:
            raise ValueError("The kicker_det signifies a draw, but no equal hands to the best hand were found")
        readable_indices = [p.ordinal(index+1) for index in best_indices]
        draw_str = p.join(readable_indices)
        win_statement = f"Draw between the {draw_str} hand ({str(best_hand)})"

    if kicker_det > -1:
        # Winner with high cards, index the hands where the high cards make a difference
        for hand_index, poker_hand in enumerate(poker_hands):
            if poker_hand.description == best_hand.description:
                best_indices.append(hand_index)
        if len(best_indices) < 2:
            raise ValueError("The kicker_det signifies a difference by kickers, but found no equal primary hand")

    # Form the string that includes the info from the single hands
    poker_hand_str = ""
    delimiter = "\n-<>-<>-<>-<>-<>-<>-<>-<>-"
    for hand_index, poker_hand in enumerate(poker_hands):
        str_printed_cards = []  # Presumes no identical cards!
        poker_hand_str += delimiter
        poker_hand_str += f'\n{p.ordinal(hand_index+1)} hand: {str(poker_hand)}'
        if hand_index == best_index:
            poker_hand_str += "\nWinning hand"
        elif hand_index in best_indices and kicker_det is -1:
            poker_hand_str += "\nHand included in the winning draw"
        poker_hand_str += "\nThe hand includes the following cards:"
        # Include main cards in the poker_hand
        for hand_card in poker_hand.hand_cards:
            kicker_str = ""
            if hand_index in best_indices and kicker_det > -1:
                # Include the kicker tag if the card plays a double role in the main hand and as a kicker
                if str(hand_card) in [str(kicker) for kicker in poker_hand.kickers[0:kicker_det]]:
                    kicker_str = ' (kicker)'
            poker_hand_str += f'\n - {str(hand_card)}{kicker_str}'
            str_printed_cards.append(str(hand_card))
        # Then include the rest of the kicker cards
        if hand_index in best_indices and kicker_det > -2:
            # This makes sure that the kicker tags are printed ->
            # also when the case is a draw with all kickers counted before determining the draw
            if kicker_det == -1:
                kicker_det = len(poker_hand.kickers) + 1
            for kicker in poker_hand.kickers[0:kicker_det]:
                if str(kicker) not in str_printed_cards:
                    poker_hand_str += f'\n - {str(kicker)} (kicker)'
                    str_printed_cards.append(str(kicker))
        # Last include the cards that do not contribute
        if poker_hand.kickers:
            for kicker in poker_hand.kickers:
                if str(kicker) not in str_printed_cards:
                    poker_hand_str += f'\n(- {str(kicker)})'

    print_string = delimiter + "\n" + win_statement + poker_hand_str + delimiter
    return print_string


class Card:
    def __init__(self, number, suit):
        self.number = number
        self.suit = suit
        if number != 1:
            self.points = number
        else:
            self.points = 14

    def __str__(self):
        return f'{num_conv(self.number)} of {self.suit}s'


class Deck:
    def __init__(self):
        self.cards = []
        for number in range(1, 14):
            for suit in ["spade", "heart", "diamond", "club"]:
                self.cards.append(Card(number, suit))
        random.shuffle(self.cards)

    def pick_card(self):
        if len(self.cards) == 0:
            raise IndexError("The deck is empty!")
        return self.cards.pop(-1)

    def get_list_of_poker_hands(self, hand_amount=3, hand_size=5):
        poker_hands_list = [HandOfCards(deck_to_use=self, card_amount=hand_size).poker_hand for _ in range(hand_amount)]
        return poker_hands_list


class PokerHand:
    """A PokerHand is a specific collection of Card objects that score in poker

    Attributes:
        description (str): A human-readable form of the scoring poker hand
        score (tuple):
            First int determines relative weighing of hands (1-10),
            second int or tuple points out the highest or determining card or cards of the hand
        hand_cards (list): Hand cards include the primary scoring cards
        kickers (list): High cards are for secondary scoring; if more than one hand has the same primary cards
        sub_hands (list): Sub_hands contain lesser hands, when the hand is formed from a combination of hands

    """
    def __init__(self, desc, score, hand_cards, kickers, sub_hands=None):
        self.description = desc
        self.score = score
        self.hand_cards = hand_cards
        self.kickers = kickers
        self.sub_hands = sub_hands

    def __str__(self):
        return self.description


class HandOfCards:
    """A collection of Card objects

    Attributes:
        cards (list): List of Card objects in the hand
        poker_hand (obj): The highest scoring PokerHand object that can be created from the Card objects

    """
    def __init__(self, deck_to_use=None, card_amount=5, test_cards=None):
        self.cards = []
        if test_cards is not None:
            self.cards = test_cards
        else:
            for _ in range(card_amount):
                self.cards.append(deck_to_use.pick_card())
        self.cards.sort(key=lambda x: x.points, reverse=True)
        self.poker_hand = self.analyse_poker_hand()

    def __str__(self):
        print_string = "Hand contains:\n-----------"
        for card in self.cards:
            print_string += f'\n{str(card)}'
        return print_string

    def analyse_poker_hand(self):
        """Analyse the highest-scoring poker hand in the hand

        Each sub-function analyzes a sub-category of poker hands reflected in function names.

        Returns:
            The PokerHand object which scores the highest and can be created from the cards in hand

        """
        hand_candidates = []

        def analyse_same_number_hands():
            """Determines high cards, pairs, threes and fours of a kind"""
            uncounted_cards = copy.deepcopy(self.cards)
            for card in self.cards:
                if str(card) in [str(x) for x in uncounted_cards]:
                    uncounted_cards.pop(0)
                    hand_cards = [card]
                    hand_card_temp_indices = []
                    for iter_index, iter_card in enumerate(copy.deepcopy(uncounted_cards)):
                        if card.number == iter_card.number:
                            hand_card_temp_indices.append(iter_index)
                    for temp_index in sorted(hand_card_temp_indices, reverse=True):
                        hand_cards.append(uncounted_cards.pop(temp_index))

                    temp_kickers = copy.deepcopy(self.cards)
                    for hand_card in hand_cards:
                        for high_card_index, kicker in enumerate(temp_kickers):
                            if str(hand_card) == str(kicker):
                                temp_kickers.pop(high_card_index)
                    kickers = sorted(temp_kickers, key=lambda x: x.number, reverse=True)

                    if len(hand_cards) == 5:
                        raise ValueError("Five of a kind? You've implemented picking from multiple decks?")
                    elif len(hand_cards) == 4:
                        hand_desc = f'Four of a kind, {num_conv(card.number, plural=True)}'
                        score = (8, card.points)
                    elif len(hand_cards) == 3:
                        hand_desc = f'Three of a kind, {num_conv(card.number, plural=True)}'
                        score = (4, card.points)
                    elif len(hand_cards) == 2:
                        hand_desc = f'Pair, {num_conv(card.number, plural=True)}'
                        score = (2, card.points)
                    elif len(hand_cards) == 1:
                        hand_desc = f'{num_conv(card.number)} high'
                        score = (1, card.points)
                    else:
                        continue
                    poker_hand = PokerHand(desc=hand_desc, score=score, hand_cards=hand_cards, kickers=kickers)
                    hand_candidates.append(poker_hand)

        def analyse_flush():
            flush = True
            suit_comparison = self.cards[0].suit
            for card in self.cards:
                if card.suit != suit_comparison:
                    flush = False
                else:
                    pass
            if flush:
                hand_desc = f'Flush, {suit_comparison}s'
                score = (6, self.cards[0].points)
                poker_hand = PokerHand(desc=hand_desc, score=score, hand_cards=self.cards, kickers=self.cards)
                hand_candidates.append(poker_hand)

        def analyse_straight():
            def check_straight(number_list):
                is_straight = True
                straight_compare = number_list.pop(0)
                for number in number_list:
                    if number == straight_compare - 1:
                        straight_compare = number
                    else:
                        is_straight = False
                return is_straight

            use_ace_as_1 = False
            straight = check_straight([x.points for x in self.cards])
            if not straight and self.cards[0].points == 14:
                straight_to_check = sorted(([x.number for x in self.cards]), reverse=True)
                straight = check_straight(straight_to_check)
                if straight:
                    use_ace_as_1 = True
            if straight:
                if use_ace_as_1:
                    hand_desc = f'Straight, 1 to 5'
                    score = (5, 5)
                else:
                    hand_desc = f'Straight, {num_conv(self.cards[-1].points)} to {num_conv(self.cards[0].points)}'
                    score = (5, self.cards[0].points)
                poker_hand = PokerHand(desc=hand_desc, score=score, hand_cards=self.cards, kickers=None)
                hand_candidates.append(poker_hand)

        def analyse_combination_hands():
            """Analyses hands consisting of lower-scoring sub-hands, e.g. Straight FLush, Two Pairs"""
            pairs = [x for x in hand_candidates if x.score[0] == 2]
            threes_of_kind = [x for x in hand_candidates if x.score[0] == 4]
            straights = [x for x in hand_candidates if x.score[0] == 5]
            flushes = [x for x in hand_candidates if x.score[0] == 6]
            kickers = []
            if len(pairs) == 2:
                pairs.sort(key=lambda x: x.score[1], reverse=True)
                hand_desc = f'Two pairs, ' \
                            f'{num_conv(pairs[0].score[1], plural=True)} and ' \
                            f'{num_conv(pairs[1].score[1], plural=True)}'
                hand_cards = pairs[0].hand_cards + pairs[1].hand_cards  # In order, higher pair first
                for card in self.cards:
                    if str(card) not in [str(x) for x in hand_cards]:
                        kickers = [card]
                score = (3, (pairs[0].score[1], pairs[1].score[1]))
                sub_hands = pairs
            elif len(threes_of_kind) == 1 and len(pairs) == 1:
                hand_desc = f'Full house, ' \
                            f'{num_conv(threes_of_kind[0].score[1], plural=True)} and ' \
                            f'{num_conv(pairs[0].score[1], plural=True)}'
                hand_cards = threes_of_kind[0].hand_cards + pairs[0].hand_cards
                kickers = None
                score = (7, (threes_of_kind[0].score[1], pairs[0].score[1]))
                sub_hands = [threes_of_kind[0], pairs[0]]
            elif len(straights) == 1 and len(flushes) == 1:
                if straights[0].score[1] == 14:
                    hand_desc = f'Royal Flush'
                else:
                    straight_desc_parts = straights[0].description.split(',')
                    hand_desc = f'{straight_desc_parts[0]} Flush,{straight_desc_parts[1]}'
                score = (9, straights[0].score[1])
                hand_cards = self.cards
                kickers = None
                sub_hands = [flushes[0], straights[0]]
            else:
                return
            poker_hand = PokerHand(desc=hand_desc, score=score,
                                   hand_cards=hand_cards, kickers=kickers,
                                   sub_hands=sub_hands)
            hand_candidates.append(poker_hand)

        analyse_same_number_hands()
        analyse_flush()
        analyse_straight()
        analyse_combination_hands()
        highest_hand, _ = order_hands(hand_candidates)
        return highest_hand


def simple_tests():
    """Runs simple tests covering some specific failures"""
    test_hand_cards = [
        # Royal Flush
        [Card(1, "club"), Card(13, "club"), Card(12, "club"), Card(11, "club"), Card(10, "club")],
        # Straight Flush
        [Card(13, "club"), Card(12, "club"), Card(11, "club"), Card(10, "club"), Card(9, "club")],
        # Four of a kind
        [Card(13, "club"), Card(13, "heart"), Card(13, "diamond"), Card(13, "spade"), Card(11, "heart")],
        # Full house
        [Card(13, "club"), Card(13, "heart"), Card(13, "diamond"), Card(11, "spade"), Card(11, "heart")],
        # Flush
        [Card(13, "club"), Card(12, "club"), Card(11, "club"), Card(7, "club"), Card(4, "club")],
        # Straight
        [Card(4, "club"), Card(5, "heart"), Card(6, "diamond"), Card(7, "spade"), Card(8, "heart")],
        # Three of a kind
        [Card(13, "club"), Card(13, "heart"), Card(13, "diamond"), Card(7, "spade"), Card(11, "heart")],
        # Two pairs
        [Card(1, "club"), Card(1, "heart"), Card(13, "diamond"), Card(11, "spade"), Card(11, "heart")],
        # Ace high, king kicker
        [Card(1, "club"), Card(13, "heart"), Card(5, "diamond"), Card(11, "spade"), Card(7, "heart")],
        # Ace high, jack kicker
        [Card(1, "club"), Card(3, "heart"), Card(5, "diamond"), Card(11, "spade"), Card(7, "heart")],
        # Ace high, jack kicker
        [Card(1, "club"), Card(3, "heart"), Card(5, "diamond"), Card(11, "spade"), Card(7, "heart")],
    ]
    test_hands_2 = [
        # Flush 2
        [Card(13, "club"), Card(12, "club"), Card(11, "club"), Card(8, "club"), Card(3, "club")],
        # Pair
        [Card(3, "club"), Card(3, "heart"), Card(5, "diamond"), Card(11, "spade"), Card(7, "heart")],
    ]
    test_hands = [
        "Royal Flush",
        "Straight Flush, 9 to King",
        "Four of a kind, Kings",
        "Full house, Kings and Jacks",
        "Flush, clubs",
        "Straight, 4 to 8",
        "Three of a kind, Kings",
        "Two pairs, Aces and Jacks",
        "Ace high",
        "Ace high",
        "Ace high",
    ]

    poker_hands = [HandOfCards(test_cards=x).poker_hand for x in test_hand_cards]
    poker_hands2 = [HandOfCards(test_cards=x).poker_hand for x in test_hands_2]

    def test_for_hand_recognition():
        for hand_index, poker_hand in enumerate(poker_hands):
            if str(poker_hand) != test_hands[hand_index]:
                print(f"Hand recognition test failed at test hand # {hand_index+1}")

    def test_for_general_hand_comparison():
        first_str_line = str_hand_comparison(poker_hands).split("\n")[2]
        if first_str_line != "The first hand wins with Royal Flush.":
            print(f"General hand comparison test failed!")

    def test_for_draw_recognition_with_only_high_cards():
        first_str_line = str_hand_comparison(poker_hands[-2:]).split("\n")[2]
        if first_str_line != "Draw between the 1st and 2nd hand (Ace high)":
            print(f"Draw recognition test failed!")

    def test_for_reporting_of_non_kicker_cards_with_same_high_cards():
        first_str_line = str_hand_comparison(poker_hands[-3:-1]).split("\n")[10]
        if first_str_line != "(- 7 of hearts)":
            print(f"High card kicker reporting test failed!")

    def test_for_reporting_of_kicker_cards_with_flushes():
        two_flushes = [poker_hands[4], poker_hands2[0]]
        ninth_str_line = str_hand_comparison(two_flushes).split("\n")[9]
        if ninth_str_line != " - 7 of clubs (kicker)":
            print(f"Flush kicker reporting test failed!")

    def test_for_reporting_of_extra_cards_with_a_pair():
        pair_and_high = [HandOfCards(test_cards=test_hands_2[1]).poker_hand,
                         HandOfCards(test_cards=test_hand_cards[-2]).poker_hand]
        ninth_str_line = str_hand_comparison(pair_and_high).split("\n")[9]
        if ninth_str_line != "(- Jack of spades)":
            print(f"Pair extra card reporting test failed!")

    def test_for_reporting_of_extra_cards_with_a_three_of_kind():
        pair_three_and_highs = [poker_hands[-3], poker_hands[6], poker_hands2[1]]
        ninth_str_line = str_hand_comparison(pair_three_and_highs).split("\n")[18]
        if ninth_str_line != "(- Jack of hearts)":
            print(f"Three of kind extra card reporting test failed!")

    test_for_hand_recognition()
    test_for_general_hand_comparison()
    test_for_draw_recognition_with_only_high_cards()
    test_for_reporting_of_non_kicker_cards_with_same_high_cards()
    test_for_reporting_of_kicker_cards_with_flushes()
    test_for_reporting_of_extra_cards_with_a_pair()
    test_for_reporting_of_extra_cards_with_a_three_of_kind()
