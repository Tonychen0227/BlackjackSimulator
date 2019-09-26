from abc import ABC, abstractmethod
from enum import Enum
import random
import uuid


class Action(Enum):
    STAY = 0
    SURRENDER = 1
    HIT = 2
    SPLIT = 3
    DOUBLE = 4


class Result(Enum):
    LOSS = 0
    PUSH = 1
    WIN = 2
    BLACKJACK = 3
    SURRENDER = 4


class Card:
    def __init__(self, suit: str, val: int):
        self.suit = suit
        self.value = val

    def printValue(self):
        if self.value >= 11:
            return 10
        return self.value

    def show(self):
        return "{} of {}".format(self.value, self.suit)


class Deck:
    def __init__(self):
        self.cards = []
        self.drawn = []
        self.build()

    def build(self):
        for s in ["Spades", "Clubs", "Diamonds", "Hearts"]:
            for v in range(1, 14):
                self.cards.append(Card(s, v))

    def shuffle(self):
        for i in range(len(self.cards) - 1, 0, -1):
            r = random.randint(0, i)
            self.cards[i], self.cards[r] = self.cards[r], self.cards[i]

    def draw(self):
        popped = self.cards.pop()
        self.drawn.append(popped)
        return popped

    def reset(self):
        for drawnCard in self.drawn:
            self.cards.append(drawnCard)
        self.shuffle()


class BlackjackPlayer(ABC):
    def __init__(self):
        self.cards = []
        self.aces = 0
        self.id = uuid.uuid4()
        pass

    def draw(self, card):
        self.cards.append(card)
        if card.printValue() == 1:
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
            temp += card.printValue()

        if temp <= 11 and self.aces >= 1:
            temp += 10

        return temp

    def print_cards(self):
        return_string = ""
        for card in self.cards:
            return_string += str(card.printValue()) + " "
        return return_string

    @abstractmethod
    def get_action(self):
        pass


class Player(BlackjackPlayer, ABC):
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
        print("Wins: {}, Pushes: {}, Surrenders: {}, Losses: {}, Bankroll: {}".format(self.wins, self.push, self.surrender, self.losses, self.bankroll))

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
