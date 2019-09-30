from deck_stuff import Deck, Card
from player_interfaces import BlackjackPlayer, Player
from basic_strategy import BasicStrategy
from dealer_strategy import DealerStrategy
import copy
from enums import Action, Result


class BlackjackGame:
    def __init__(self, decks: int):
        self.deck = Deck()
        self.players = []
        self.dealer = Dealer()
        for x in range(0, decks):
            self.deck.build()

    def add_player(self, player: BlackjackPlayer):
        self.players.append(player)

    def remove_player(self, player: BlackjackPlayer):
        self.players.pop(self.players.index(player))

    def play_hand(self):
        secondary_players = {}

        self.deck.reset()
        if not self.deck.check_integrity():
            raise Exception("Deck has been compromised")
        self.dealer.reset()

        for player in self.players:
            try:
                player.start_hand()
            except Exception:
                self.remove_player(player)
                print("Player: {} eliminated".format(player.id))
                if len(self.players) == 0:
                    raise Exception("No players remaining")
            continue
            player.draw(self.deck.draw())

        self.dealer.draw(self.deck.draw())

        for player in self.players:
            player.draw(self.deck.draw())
        self.dealer.draw(self.deck.draw())

        dealer_card = self.dealer.reveal()

        print("Dealer card: ", dealer_card.print_value())
        for player in self.players:
            if self.dealer.has_blackjack() and player.has_blackjack():
                print("Push: both players blackjack")
                player.pay(Result.PUSH)
                continue

            if self.dealer.has_blackjack():
                print("Loss: dealer blackjack")
                player.pay(Result.LOSS)
                continue

            if player.has_blackjack():
                print("Win: player blackjack")
                player.pay(Result.BLACKJACK)
                continue

            action = None
            while not player.check_bust():
                action = player.get_strategy_action(dealer_card)
                if len(player.cards) == 1:
                    action = Action.HIT

                if action == Action.HIT:
                    player.draw(self.deck.draw())
                elif action == Action.DOUBLE:
                    if not player.try_bet(player.wager):
                        player.cards.append(Card("dummy", 0))
                    else:
                        player.draw(self.deck.draw())
                        player.double_wager()
                        break
                elif action == Action.SPLIT:
                    if not player.try_bet(player.wager):
                        player.cards.append(Card("dummy", 0))
                    else:
                        player.draw(self.deck.draw())
                        player.cards = [player.cards[0]]
                        secondary_player = copy.deepcopy(player)
                        secondary_player.bankroll = 0
                        if player.id in secondary_players:
                            dummy_array = secondary_players[player.id]
                        else:
                            dummy_array = []
                        if player.cards[0].value == 1:
                            #One card only, no blackjack
                            secondary_player.cards = [player.cards[0]]
                            secondary_player.draw(self.deck.draw())
                            dummy_array.append(secondary_player)
                            secondary_players[player.id] = dummy_array
                            player.draw(self.deck.draw())
                            break
                        else:
                            self.simulate_secondary(player, secondary_player, dummy_array, dealer_card)
                        secondary_players[player.id] = dummy_array
                        player.draw(self.deck.draw())
                elif action == Action.STAND:
                    break
                elif action == Action.SURRENDER:
                    player.pay(Result.SURRENDER)
                    break

        while not self.dealer.check_bust():
            action = self.dealer.get_action()
            if action == Action.HIT:
                self.dealer.draw(self.deck.draw())
            elif action == Action.STAND:
                break

        dealer_count = self.dealer.get_final_sum()

        print("Dealer with final cards: " + self.dealer.print_cards())

        for player in self.players:
            if player.id in secondary_players:
                for secondary_player in secondary_players[player.id]:
                    if secondary_player.bankroll != 0:
                        player.bankroll += secondary_player.bankroll
                        continue
                    print("Split player: {} with final cards: {}".format(player.id, secondary_player.print_cards()))
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

    def simulate_secondary(self, primary_player: Player, player: Player, dummy_array, dealer_card: Card):
        player.id = "Secondary"
        player.draw(self.deck.draw())
        while not player.check_bust():
            action = player.get_strategy_action(dealer_card)

            if len(player.cards) == 1:
                action = Action.HIT

            if action == Action.HIT:
                player.draw(self.deck.draw())
            elif action == Action.DOUBLE:
                if not primary_player.try_bet(player.wager):
                    player.cards.append(Card("dummy", 0))
                else:
                    player.draw(self.deck.draw())
                    player.double_wager()
                    break
            elif action == Action.SPLIT:
                if not primary_player.try_bet(player.wager):
                    player.cards.append(Card("dummy", 0))
                else:
                    player.draw(self.deck.draw())
                    player.cards = [player.cards[0]]
                    secondary_player = copy.deepcopy(player)
                    secondary_player.bankroll = 0
                    if player.cards[0].value == 1:
                        # One card only, no blackjack
                        secondary_player.cards = [player.cards[0]]
                        secondary_player.draw(self.deck.draw())
                        dummy_array.append(secondary_player)
                    else:
                        self.simulate_secondary(primary_player, secondary_player, dummy_array, dealer_card)
                    player.draw(self.deck.draw())
            elif action == Action.STAND:
                break
            elif action == Action.SURRENDER:
                player.pay(Result.SURRENDER)
                break
        dummy_array.append(player)


class Dealer(BlackjackPlayer):
    def __init__(self):
        super().__init__("dealer")

    def reveal(self):
        return self.cards[0]

    def get_action(self):
        action = DealerStrategy.get_action(self.cards, self.aces)
        print("Player: {} with cards: {} chose: {}".format(self.id, self.print_cards(), action))
        return action


class BasicStrategyNaivePlayer(Player):
    def __init__(self, bankroll: int, basewager: int):
        super().__init__("Basic Strategy Naive", bankroll, basewager)

    def get_wager(self):
        return min(self.basewager, self.bankroll)

    def get_strategy_action(self, dealer_card: Card):
        action = BasicStrategy.get_action(self.cards, self.aces, dealer_card)
        print("Player: {} with cards: {} chose: {}".format(self.id, self.print_cards(), action))
        return action

    def record_wager(self, wager: int, result: Result):
        pass


class BasicStrategyLaboucherePlayer(Player):
    def __init__(self, bankroll: int, basewager: int):
        super().__init__("Basic Strategy Labouchere", bankroll, basewager)
        self.bet_array = []
        self.generate_array(basewager, 10)

    def get_wager(self):
        if len(self.bet_array) == 1:
            wager = self.bet_array[0]
        else:
            wager = self.bet_array[1] + self.bet_array[-1]

        return min(wager, self.bankroll)

    def get_strategy_action(self, dealer_card: Card):
        action = BasicStrategy.get_action(self.cards, self.aces, dealer_card)
        print("Player: {} with cards: {} chose: {}".format(self.id, self.print_cards(), action))
        return action

    def record_wager(self, wager: int, result: Result):
        if result == Result.BLACKJACK or result == Result.WIN:
            if len(self.bet_array) == 1 or len(self.bet_array) == 2:
                self.generate_array(self.basewager, 10)
            else:
                self.bet_array = self.bet_array[1:-1]
        elif result == Result.LOSS or result == Result.SURRENDER:
            self.bet_array.append(wager)
        
            if sum(self.bet_array) / len(self.bet_array) > self.basewager * 5:
                self.generate_array(self.basewager, int(sum(self.bet_array)/self.basewager))
            else:
                if wager > self.basewager * 5:
                    self.bet_array = self.bet_array[0:-1]
                    self.bet_array.append(wager // 2)
                    self.bet_array.append(wager // 2)
                
        print(self.bet_array)

    def generate_array(self, amount, count):
        self.bet_array = []
        for x in range(1, count):
            self.bet_array.append(amount)


class ManualPlayer(Player):
    def __init__(self, id: str, bankroll: int, basewager: int):
        super().__init__(id, bankroll, basewager)

    def get_wager(self):
        wager = 0

        while wager <= 0 or wager > self.bankroll:
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
                0: Action.STAND,
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
            if self.bankroll < self.wager * 2:
                return False
            return True
        elif action == Action.DOUBLE:
            if len(self.cards) > 2:
                return False
            if self.bankroll < self.wager * 2:
                return False
            return True
        elif action == Action.STAND or action == Action.HIT or action == action.SURRENDER:
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
    while want_manual == 1:
        name = input("Input player name: ")
        game.add_player(ManualPlayer(name, starting_bank, starting_wager))
        want_manual = int(input("Do you want to add another manual player? 1 for yes, 0 for no: "))

    want_automatic = int(input("Do you want to add a automatic basic strategy player? 1 for yes, 0 for no: "))
    if want_automatic == 1:
        game.add_player(BasicStrategyNaivePlayer(starting_bank, starting_wager))

    want_labouchere = int(input("Do you want to add a automatic basic strategy labouchere player? 1 for yes, 0 for no: "))
    if want_labouchere == 1:
        game.add_player(BasicStrategyLaboucherePlayer(starting_bank, starting_wager))

    for x in range(0, hands):
        game.play_hand()

    for player in game.players:
        player.print_status()


main()
