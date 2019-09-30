from abc import ABC, abstractmethod
from deck_stuff import Card
from enums import Result


class BlackjackPlayer(ABC):
    def __init__(self, id: str):
        self.id = id
        self.cards = []
        self.aces = 0
        pass

    def draw(self, card):
        self.cards.append(card)
        if card.print_value() == 1:
            self.aces += 1

    def reset(self):
        self.cards = []
        self.aces = 0

    def check_bust(self):
        return self.get_final_sum() > 21

    def has_blackjack(self):
        return self.aces == 1 and self.get_final_sum() == 21

    def get_final_sum(self):
        temp = 0
        for card in self.cards:
            temp += card.print_value()

        if temp <= 11 and self.aces >= 1:
            temp += 10

        return temp

    def print_cards(self):
        return_string = ""
        for card in self.cards:
            return_string += str(card.print_number()) + " "
        return return_string

    @abstractmethod
    def get_action(self):
        pass


class Player(BlackjackPlayer, ABC):
    def __init__(self, id: str, bankroll: int, basewager: int):
        super().__init__(id)
        self.bankroll = bankroll
        self.basewager = basewager
        self.wager = basewager
        self.wins = 0
        self.push = 0
        self.surrender = 0
        self.losses = 0
        self.blackjacks = 0

    def try_bet(self, bet: int):
        if self.bankroll - bet < 0:
            return False
        else:
            self.bankroll -= bet
            return True

    def get_action(self):
        pass

    @abstractmethod
    def get_wager(self):
        pass

    @abstractmethod
    def record_wager(self, wager: int, result: Result):
        pass

    @abstractmethod
    def get_strategy_action(self, dealer_card: Card):
        pass

    def double_wager(self):
        self.wager *= 2

    def iterator_helper(self, x):
        return str(x)

    def print_status(self):
        print("Player: {} Blackjack Wins: {}, Wins: {}, Pushes: {}, Surrenders: {}, Losses: {}, Bankroll: {}".format(self.id, self.blackjacks
                                                      , self.wins, self.push, self.surrender, self.losses, self.bankroll))

    def start_hand(self):
        if self.bankroll <= 0:
            raise Exception("dead")
        print("Player {} Bankroll: {}".format(self.id, self.bankroll))
        self.wager = self.get_wager()
        self.bankroll -= self.wager

    def pay(self, result: Result):
        if result == Result.BLACKJACK:
            self.bankroll += self.wager * 2.5
            self.blackjacks += 1
        elif result == Result.LOSS:
            self.losses += 1
        elif result == Result.SURRENDER:
            self.bankroll += self.wager * 0.5
            self.surrender += 1
        elif result == Result.WIN:
            self.bankroll += self.wager * 2
            self.wins += 1
        else:
            self.bankroll += self.wager * 1
            self.push += 1
        self.record_wager(self.wager, result)
        self.reset()
