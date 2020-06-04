import functions as gf
from dealer import Dealer
from player import Player


# runs 1000 rounds of the game and prints the stats at the end to see how well the AI did
# first the dealer shuffles the deck and prints out the shuffled deck at the beginning
# at the beginning of a round, will display round number and the initial hands of both the dealer and the player
# will then check the naturals of both the player and the dealer and see if there is a winner early
# if not, then it is now the players turn; after the players turn, the dealer will then go until he hits 17 or busts
# a winner is assigned and the round resets.
# if the cards played gets above 225, which is about 4 decks, it will do a reset shuffle(make it back to 6 decks)
# once it reaches 1000 rounds, it will display the stats for the run as mentioned before
def run_game():
    dealer = Dealer()
    player = Player()
    round_num = 1
    in_progress = True

    print("--Welcome to Blackjack AI!--")
    dealer.full_shuffle()
    print(dealer.full_deck)
    while in_progress:
        gf.declare_round(round_num)
        dealer.initial_deal(player)
        gf.show_hands(player, dealer)

        dealer.maybe_natural(player)
        gf.check_naturals(player, dealer)
        if player.natural or dealer.natural:
            gf.natural_winner(player, dealer)

        if not player.winner and not dealer.winner and not dealer.tie:
            player.ai_turn(dealer)
            if not dealer.winner:
                dealer.dealer_move(player)
                if not player.winner:
                    gf.assign_winner(player, dealer)
        gf.declare_winner(player, dealer)

        gf.reset_round(player, dealer)
        round_num += 1
        if player.card_total > 225:
            dealer.reset_shuffle(player)
        if round_num == 1000:
            in_progress = False
        print("----------------------------------------------")
    print("AI Wins:     {}".format(player.win_count))
    print("Ties:        {}".format(player.tie_count))
    print("Dealer Wins: {}".format(player.dealer_win_count))
    print("Bankroll:    {}".format(player.bankroll))


run_game()
