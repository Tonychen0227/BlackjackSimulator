from abstractions import BlackjackPlayer, Action, Result, Deck, Card
from basic_strategy import BasicStrategy


class BlackjackGame:
    def __init__(self, decks: int):
        self.deck = Deck()
        self.players = []
        self.dealer = Dealer()
        for x in range(0, decks):
            self.deck.build()

    def add_player(self, player: BlackjackPlayer):
        self.players.append(player)

    def play_hand(self):
        secondary_players = {}

        self.deck.shuffle()

        for player in self.players:
            player.draw(self.deck.draw())

        self.dealer.draw(self.deck.draw())

        for player in self.players:
            player.draw(self.deck.draw())
        self.dealer.draw(self.deck.draw())

        dealer_card = self.dealer.reveal()

        print("Dealer card: ", dealer_card.show())
        for player in self.players:
            if self.dealer.has_blackjack() and player.has_blackjack():
                print("Mutual blackjack")
                player.pay(Result.PUSH)
                continue

            if self.dealer.has_blackjack():
                print("You lost to blackjack")
                player.pay(Result.LOSS)

            if player.has_blackjack():
                print("You got blackjack")
                player.pay(Result.BLACKJACK)

            while not player.check_bust():
                action = player.get_strategy_action(dealer_card)
                print("Player: ", player.id, "Your cards: ", player.print_cards(), "You chose: ", action)
                if len(player.cards) == 1:
                    action = Action.HIT

                if action == Action.HIT:
                    player.draw(self.deck.draw())
                elif action == Action.DOUBLE:
                    player.draw(self.deck.draw())
                    player.double_wager()
                elif action == Action.SPLIT:
                    print("split")
                    player.cards = [player.cards[0]]
                    dummy_array = []
                    self.simulate_secondary(dummy_array, player.cards[0], player.wager, dealer_card)
                    secondary_players[player.id] = dummy_array
                elif action == Action.STAY:
                    break
                elif action == Action.SURRENDER:
                    player.pay(Result.SURRENDER)
                    break

        while not self.dealer.check_bust():
            action = self.dealer.get_action()
            if action == Action.HIT:
                self.dealer.draw(self.deck.draw())
            elif action == Action.STAY:
                break

        dealer_count = self.dealer.get_final_sum()

        for player in self.players:
            if len(player.cards) == 0:
                continue
            player_count = player.get_final_sum()
            if player_count > 21:
                print("You Bust: {} vs {}".format(player_count, dealer_count))
                player.pay(Result.LOSS)
            elif dealer_count > 21:
                print("Dealer Bust: {} vs {}".format(player_count, dealer_count))
                player.pay(Result.WIN)
            elif player_count > dealer_count:
                print("Win: {} vs {}".format(player_count, dealer_count))
                player.pay(Result.WIN)
            elif player_count == dealer_count:
                print("Push: {} vs {}".format(player_count, dealer_count))
                player.pay(Result.PUSH)
            else:
                print("Loss: {} vs {}".format(player_count, dealer_count))
                player.pay(Result.LOSS)

            if player.id in secondary_players:
                for secondary_player in secondary_players[player.id]:
                    if secondary_player.bankroll != 0:
                        player.bankroll += secondary_player.bankroll
                        continue

                    value = secondary_player.get_final_sum()
                    if value > 21:
                        print("(SPLIT HAND) You Bust: {} vs {}".format(value, dealer_count))
                        secondary_player.pay(Result.LOSS)
                    elif dealer_count > 21:
                        print("(SPLIT HAND) Dealer Bust: {} vs {}".format(value, dealer_count))
                        secondary_player.pay(Result.WIN)
                    elif value > dealer_count:
                        print("(SPLIT HAND) Win: {} vs {}".format(value, dealer_count))
                        secondary_player.pay(Result.WIN)
                    elif value == dealer_count:
                        print("(SPLIT HAND) Push: {} vs {}".format(value, dealer_count))
                        secondary_player.pay(Result.PUSH)
                    else:
                        print("(SPLIT HAND) Loss: {} vs {}".format(value, dealer_count))
                        secondary_player.pay(Result.LOSS)

                    player.bankroll += secondary_player.bankroll
            print("Player {} Bankroll: {}".format(player.id, player.bankroll))
        self.dealer.reset()

    def simulate_secondary(self, dummy_array, card: Card, wager: int, dealer_card: Card):
        player = Player(0, wager)
        player.cards = [card]
        while not player.check_bust():
            action = player.get_strategy_action(dealer_card)
            print("Player: ", player.id, "Your cards: ", player.print_cards(), "You chose: ", action)

            if len(player.cards) == 1:
                action = Action.HIT

            if action == Action.HIT:
                player.draw(self.deck.draw())
            elif action == Action.DOUBLE:
                player.draw(self.deck.draw())
                player.double_wager()
            elif action == Action.SPLIT:
                player.cards = [player.cards[0]]
                self.simulate_secondary(dummy_array, player.cards[0], player.wager, dealer_card)
            elif action == Action.STAY:
                break
            elif action == Action.SURRENDER:
                player.pay(Result.SURRENDER)
                break
        dummy_array.append(player)

class Dealer(BlackjackPlayer):
    def reveal(self):
        return self.cards[0]

    def get_action(self):
        sum_so_far = 0
        for card in self.cards:
            sum_so_far += card.printValue()

        if sum_so_far >= 17:
            return Action.STAY

        if self.aces >= 1 and sum_so_far <= 11:
            sum_so_far += 10

        if sum_so_far >= 17:
            return Action.STAY

        return Action.HIT


class Player(BlackjackPlayer):
    def __init__(self, bankroll: int, basewager: int):
        super().__init__()
        self.bankroll = bankroll
        self.basewager = basewager
        self.wager = basewager
        self.wins = 0
        self.push = 0
        self.surrender = 0
        self.losses = 0
        self.blackjacks = 0


    def get_action(self):
        return Action.STAY

    def get_strategy_action(self, dealer_card: Card):
        return BasicStrategy.get_action(self.cards, self.aces, dealer_card)

    def double_wager(self):
        self.wager *= 2

    def iterator_helper(self, x):
        return str(x)

    def print_status(self):
        print(','.join(map(self.iterator_helper, [self.wins, self.push, self.surrender, self.losses, self.blackjacks])))

    def pay(self, result: Result):
        if result == Result.BLACKJACK:
            self.bankroll += self.wager * 1.5
            self.blackjacks += 1
        elif result == Result.LOSS:
            self.bankroll += self.wager * -1
            self.losses += 1
        elif result == Result.SURRENDER:
            self.bankroll += self.wager * 0.5
            self.surrender += 1
        elif result == Result.WIN:
            self.bankroll += self.wager
            self.wins += 1
        else:
            self.push += 1

        self.wager = self.basewager
        self.reset()


def main(decks, hands):
    game = BlackjackGame(decks)
    player = Player(20, 1)
    game.add_player(player)

    for x in range(0, hands):
        game.play_hand()

    print(player.print_status())
    print(player.bankroll)

main(6, 10)
