import functions as gf


# initializes necessary parameters such as the hand total, the betting, etc.
class Player:

    def __init__(self):
        self.cards_in_hand = []
        self.winner = False
        self.hand_total = 0       # hand total if there is an ace and you want a 11
        self.hand_total_alt = 0   # hand total if there is an ace and you want a 1
        self.natural = False
        self.assumption = 0       # what we assume the dealer's current hand is
        self.true_assumption = 0  # what we assume the dealer's final hand is
        self.win_count = 0
        self.tie_count = 0
        self.dealer_win_count = 0

        self.bankroll = 10000     # starting amt of money
        self.betAmount = 0
        self.running_total = 0    # current total using card counting method
        self.true_total = 0       # running total divided by amount of decks
        self.card_total = 0       # total cards accounted for so far

    # main function for the AI functionality
    # first it gets the bet amount and the opponents probability of busting and the ai_probability of busting
    # then it checks if the dealer's hole is down;
    # if so it assumes that the face down is a value of 10 bc of basic Blackjack strategy
    # the AI will always assume that the dealer may get at least 17 so it puts that as the true assumption
    def ai_turn(self, dealer):
        stay = False
        self.betAmount = gf.determine_bet_amt(self)  # update how much is bet for the round
        print("Bankroll:  {} ".format(self.bankroll))
        print("Bet Amount: {} ".format(self.betAmount))

        decision = " "
        opponent_prob = gf.bust_prob(dealer.hand_total, dealer)
        ai_prob = gf.bust_prob(self.hand_total, dealer)

        if dealer.hole_down is True:
            self.assumption = gf.card_values(dealer.cards_in_hand[0]) + 10
        else:
            self.assumption = dealer.hand_total

        if self.assumption < 17:
            self.true_assumption = 17
        else:
            self.true_assumption = self.assumption

        print("----AI's Turn----")

        # if the AI has a hand between 17 and 21 then it will stay bc that is considered a good hand
        # if assumption < 17, then if the probability of busting is lower than the opponent's,
        # then it will decide to hit/dd, else it will stay
        # if decision was to DD then the AI stays and if the AI busted after hitting/dd,
        # then it will print bust and the dealer wins
        # else if the assumption is over 17 and the hand total isnt between 17 and 21, then the AI will hit/dd
        while stay is False:
            if 17 <= self.hand_total <= 21 or 17 <= self.hand_total_alt <= 21:
                stay = True
                print("STAY")
            elif self.assumption < 17:
                if ai_prob == 0 or (.5 > opponent_prob >= ai_prob):
                    decision = gf.hit_or_dd(self.hand_total, self.hand_total_alt, self.true_assumption,
                                            self.cards_in_hand, dealer, self)
                    if decision == "DD":
                        stay = True
                    gf.calc_hand_total(self)
                    if gf.check_bust(self.hand_total_alt):
                        stay = True
                        print("BUST")
                        dealer.winner = True
                else:
                    stay = True
                    print("STAY")
            else:
                decision = gf.hit_or_dd(self.hand_total, self.hand_total_alt,
                                        self.true_assumption, self.cards_in_hand, dealer, self)
                if decision == "DD":
                    stay = True
                gf.calc_hand_total(self)
                if gf.check_bust(self.hand_total_alt):
                    stay = True
                    print("BUST")
                    dealer.winner = True

            gf.show_hands(self, dealer)
