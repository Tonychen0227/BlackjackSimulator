from abc import ABC, abstractmethod
from enum import Enum
import random
import uuid


class BlackjackPlayer(ABC):
    def __init__(self):
        self.cards = []
        self.aces = 0
        self.id = uuid.uuid4()
        pass

    def draw(self, card):
        self.cards.append(card)

    def reset(self):
        self.cards = []
        self.aces = 0

    def check_bust(self):
        return self.get_final_sum() - self.aces * 10 > 21

    def has_blackjack(self):
        return self.aces == 1 and self.get_final_sum() == 14

    def get_final_sum(self):
        temp = 0
        for card in self.cards:
            temp += card.printValue()

        if temp <= 11 and self.aces >= 1:
            temp += 11

        return temp

    def print_cards(self):
        return_string = ""
        for card in self.cards:
            return_string += str(card.printValue()) + " "
        return return_string

    @abstractmethod
    def get_action(self):
        pass


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
