import functions as gf


# initializes the deck, all of the individual card counts, its hand total, if it needs to hole down, etc.
class Dealer:

    def __init__(self):
        self.winner = False
        self.deck = ['SA', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8', 'S9', 'S10', 'SJ', 'SQ', 'SK',
                     'CA', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10', 'CJ', 'CQ', 'CK',
                     'HA', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9', 'H10', 'HJ', 'HQ', 'HK',
                     'DA', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10', 'DJ', 'DQ', 'DK']
        self.full_deck = self.deck + self.deck + self.deck + self.deck + self.deck + self.deck
        self.cards_in_hand = []
        self.hand_total = 0         # hand total if there is an ace and you want a 11
        self.hand_total_alt = 0     # hand total if there is an ace and you want a 1
        self.full_deck_total = 312  # total cards in the deck

        # number of each card in the deck
        self.tens = 96
        self.nines = 24
        self.eights = 24
        self.sevens = 24
        self.sixes = 24
        self.fives = 24
        self.fours = 24
        self.threes = 24
        self.twos = 24
        self.aces = 24

        self.true_hand_total = 0  # final decision of what hard total to use
        self.true_hand_decided = False
        self.natural = False
        self.tie = False
        self.hole_down = True  # second dealer card face down

    # shuffles the entire full deck(6 decks shuffled together)
    def full_shuffle(self):
        for x in range(5):
            self.full_deck = gf.shuffle(self.full_deck)

    # resets the deck and puts all values back to their original values before playing
    def reset_shuffle(self, player):
        self.full_deck = self.deck + self.deck + self.deck + self.deck + self.deck + self.deck
        self.full_shuffle()
        self.full_deck_total = 312
        self.tens = 96
        self.nines = 24
        self.eights = 24
        self.sevens = 24
        self.sixes = 24
        self.fives = 24
        self.fours = 24
        self.threes = 24
        self.twos = 24
        self.aces = 24
        player.running_total = 0
        player.true_total = 0
        player.card_total = 0

    # dealer deals the first cards to themselves and the player
    def initial_deal(self, player):
        gf.remove_from_deck_count(self.full_deck[0], self, player)
        gf.remove_from_deck_count(self.full_deck[1], self, player)
        gf.remove_from_deck_count(self.full_deck[2], self, player)
        for i in range(2):
            player.cards_in_hand.append(self.full_deck.pop(0))
            self.cards_in_hand.append(self.full_deck.pop(0))

    # resets the player and dealer's hands after a round is over
    def reset_hands(self, player):
        player.cards_in_hand = []
        self.cards_in_hand = []

    # code for when it's the dealers turn
    # dealer gets his cards and shows what he has;
    # then goes into a while loop that ends once it decides what its hand is
    # if its total is between 17 and 21 then it stays and while loop is exited, if its under 17 then it needs to hit
    # will then check if its busted(goes over 21)
    def dealer_move(self, player):
        print("----Dealer Turn----")
        gf.calc_hand_total(self)
        self.hole_down = False
        gf.remove_from_deck_count(self.cards_in_hand[1], self, player)
        gf.show_hands(player, self)
        while not self.true_hand_decided:
            if 17 <= self.hand_total <= 21:
                self.true_hand_total = self.hand_total
                self.true_hand_decided = True
            elif self.hand_total < 17 or self.hand_total_alt < 17:
                gf.hit(self.cards_in_hand, self, player)
                gf.calc_hand_total(self)
                gf.show_hands(player, self)
            else:
                self.true_hand_total = self.hand_total_alt
                self.true_hand_decided = True
        if gf.check_bust(self.true_hand_total):
            player.winner = True
            print("BUST")

    # if a card is a 10, face, or an ace, then the dealer will show both of his cards before the player gets to play
    def maybe_natural(self, player):
        card = self.cards_in_hand[0]
        num = card[-1]
        if num == '0' or num == 'J' or num == 'Q' or num == 'K' or num == 'A':
            self.hole_down = False
            gf.remove_from_deck_count(self.cards_in_hand[1], self, player)
            gf.show_hands(player, self)
