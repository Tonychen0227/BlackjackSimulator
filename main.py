from abstractions import BlackjackPlayer, Action, Result, Deck, Card, Player
from basic_strategy import BasicStrategy
import copy


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
        self.dealer.reset()

        for player in self.players:
            player.start_hand()
            player.draw(self.deck.draw())

        self.dealer.draw(self.deck.draw())

        for player in self.players:
            player.draw(self.deck.draw())
        self.dealer.draw(self.deck.draw())

        dealer_card = self.dealer.reveal()

        print("Dealer card: ", dealer_card.printValue())
        for player in self.players:
            if self.dealer.has_blackjack() and player.has_blackjack():
                print("Push: both players blackjack")
                player.pay(Result.PUSH)
                continue

            if self.dealer.has_blackjack():
                print("Loss: dealer blackjack")
                player.pay(Result.LOSS)

            if player.has_blackjack():
                print("Win: player blackjack")
                player.pay(Result.BLACKJACK)

            action = None
            while not player.check_bust() and action != Action.DOUBLE:
                action = player.get_strategy_action(dealer_card)
                if len(player.cards) == 1:
                    action = Action.HIT

                if action == Action.HIT:
                    player.draw(self.deck.draw())
                elif action == Action.DOUBLE:
                    player.draw(self.deck.draw())
                    player.double_wager()
                elif action == Action.SPLIT:
                    player.cards = [player.cards[0]]
                    secondary_player = copy.deepcopy(player)
                    secondary_player.bankroll = 0
                    dummy_array = []
                    self.simulate_secondary(secondary_player, dummy_array, dealer_card)
                    secondary_players[player.id] = dummy_array
                    player.draw(self.deck.draw())
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

        print("Dealer with final cards: " + self.dealer.print_cards())

        for player in self.players:
            if player.id in secondary_players:
                for secondary_player in secondary_players[player.id]:
                    if secondary_player.bankroll != 0:
                        player.bankroll += secondary_player.bankroll
                        continue
                    print("Split player: {} with final cards: {}".format(player.id, player.print_cards()))
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

            if len(player.cards) == 0:
                continue

            print("Player: {} with final cards: {}".format(player.id, player.print_cards()))
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

    def simulate_secondary(self, player: Player, dummy_array, dealer_card: Card):
        player.id = "Secondary"
        player.draw(self.deck.draw())
        action = None
        while not player.check_bust() and action != Action.DOUBLE:
            action = player.get_strategy_action(dealer_card)

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


class BasicStrategyPlayer(Player):
    def __init__(self, type: str, bankroll: int, basewager: int):
        super().__init__(bankroll, basewager)
        self.id = type

    def get_wager(self):
        return self.basewager

    def get_strategy_action(self, dealer_card: Card):
        action = BasicStrategy.get_action(self.cards, self.aces, dealer_card)
        print("Player: {} with cards: {} chose: {}".format(self.id, self.print_cards(), action))
        return action

    def record_wager(self, wager: int, result: Result):
        pass

class ManualPlayer(Player):
    def __init__(self, type: str, bankroll: int, basewager: int):
        super().__init__(bankroll, basewager)
        self.id = type

    def get_wager(self):
        wager = 0

        while wager <= 0:
            wager = int(input("Select your next wager. Must > 0: "))

        return wager

    def get_strategy_action(self, dealer_card: Card):
        print("Player: {} with cards: {}".format(self.id, self.print_cards()))
        action = None

        while not self.check_valid_action(action):
            if action is not None:
                print("Last action was invalid. Trying again.")
            action_int = int(input("Select an action. STAY = 0, SURRENDER = 1, HIT = 2, SPLIT = 3, DOUBLE DOWN = 4: "))
            return_dict = {
                0: Action.STAY,
                1: Action.SURRENDER,
                2: Action.HIT,
                3: Action.SPLIT,
                4: Action.DOUBLE
            }
            try:
                action = return_dict[action_int]
            except KeyError:
                action = None

        print("Basic Strategy Suggested Action: ", BasicStrategy.get_action(self.cards, self.aces, dealer_card))
        print("You chose: ", return_dict[action_int])

        return action

    def check_valid_action(self, action: Action):
        if action is None:
            return False

        if action == Action.SPLIT:
            if len(self.cards) > 2 or self.cards[0].value != self.cards[1].value:
                return False
            return True
        elif action == Action.DOUBLE:
            if len(self.cards) > 2:
                return False
            return True
        elif action == Action.STAY or action == Action.HIT or action == action.SURRENDER:
            return True
        return False

    def record_wager(self, wager: int, result: Result):
        pass

def main():
    hands = int(input("How many hands do you want to play? "))
    decks = int(input("How many decks do you want to use? This is a CSM (continuous shuffling machine): "))

    game = BlackjackGame(decks)
    starting_bank = int(input("What starting bankroll do you want? "))
    starting_wager = int(input("What starting wager do you want? "))
    want_manual = int(input("Do you want to add a manual player? 1 for yes, 0 for no: "))
    if want_manual == 1:
        player1 = ManualPlayer("Manual", starting_bank, starting_wager)
        game.add_player(player1)

    want_automatic = int(input("Do you want to add a automatic basic strategy player? 1 for yes, 0 for no: "))
    if want_automatic == 1:
        player2 = BasicStrategyPlayer("Basic Strategy", starting_bank, starting_wager)
        game.add_player(player2)

    for x in range(0, hands):
        game.play_hand()

    for player in game.players:
        player.print_status()


main()
