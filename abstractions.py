from abc import ABC, abstractmethod
from enum import Enum


class BlackjackPlayer(ABC):
    def __init__(self):
        self.cards = []
        self.possiblesums = [0]
        self.aces = 0
        pass

    def draw(self, card):
        self.cards.append(card)
        additionalValue = card.printValue()
        self.cardsum[0] += card.printValue()
        if additionalValue == 1:
            self.possiblesums.append(self.cardsum[0] + 10)

    def reset(self):
        self.cards = []

    def check_bust(self):
        return self.cardsum - self.aces * 10 > 21

    def has_blackjack(self):
        return self.aces == 1 and self.cardsum == 14

    @abstractmethod
    def get_action(self):
        pass


class Action(Enum):
    STAY = 0
    SURRENDER = 1
    HIT = 2
    SPLIT = 3
    DOUBLE = 4