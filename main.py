import random

from abstractions import BlackjackPlayer, Action
from basic_strategy import BasicStrategy


class Card:
    def __init__(self, suit, val):
        self.suit = suit
        self.value = val

    def printValue(self):
        if self.val >= 11:
            return 10
        return int(self.val)

    def show(self):
        print("{} of {}".format(self.value, self.suit))


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


class BlackjackGame:
    def __init__(self, decks):
        self.deck = Deck()
        self.players = []
        self.dealer = Dealer()
        for x in range(0, decks):
            self.deck.build()

    def addPlayer(self, player):
        self.players.append(player)

    def startHand(self):
        self.deck.shuffle()

        self.dealer.reset()
        for player in self.players:
            player.reset()

        self.dealer.draw(self.deck.draw())


class Dealer(BlackjackPlayer):
    def reveal(self):
        return self.cards[0]

    def get_action(self):
        for sum in self.possiblesums:
            if sum >= 17 and sum <= 31:
                return Action.STAY
        return Action.HIT


class Player(BlackjackPlayer):
    def get_action(self):
        return BasicStrategy.get_action([], 0, Card(0, "suit"))


def main(decks, hands):
    game = BlackjackGame(decks)

    for x in range(0, hands):
        game.startHand()


main(6)