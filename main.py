import random

from abstractions import BlackjackPlayer, Action
from basic_strategy import BasicStrategy


class Card:
    def __init__(self, suit: str, val: int):
        self.suit = suit
        self.value = val

    def printValue(self):
        if self.value >= 11:
            return 10
        return self.value

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
    def __init__(self, decks: int):
        self.deck = Deck()
        self.players = []
        self.dealer = Dealer()
        for x in range(0, decks):
            self.deck.build()

    def addPlayer(self, player: BlackjackPlayer):
        self.players.append(player)

    def startHand(self):
        self.deck.shuffle()

        self.dealer.reset()
        for player in self.players:
            player.reset()

        self.dealer.draw(self.deck.draw())
        for player in self.players:
            player.draw(self.deck.draw())

        self.dealer.draw(self.deck.draw())
        for player in self.players:
            if player.has_blackjack() and not self.dealer.has_blackjack():
                player.pay(0)
                player.reset()
                continue

            while not player.check_bust():
                action = player.get_action()
                if action == Action.HIT:
                    player.draw(self.deck.draw())
                elif action == Action.DOUBLE:
                    player.draw(self.deck.draw())
                    player.double_wager()
                elif action == Action.SPLIT:
                    pass
                elif action == Action.STAY:
                    continue
                elif action == Action.SURRENDER:
                    player.pay(0)
                    player.reset()
                    continue


class Dealer(BlackjackPlayer):
    def reveal(self):
        return self.cards[0]

    def get_action(self):
        for possibleSum in self.possiblesums:
            if possibleSum >= 17 and possibleSum <= 31:
                return Action.STAY
        return Action.HIT


class Player(BlackjackPlayer):
    def __init__(self, bankroll: int):
        self.bankroll = bankroll
        self.wager = 0

    def get_action(self):
        return Action.STAY

    def get_strategy_action(self, dealer_card: Card):
        return BasicStrategy.get_action(self.cards, self.aces, dealer_card)

    def double_wager(self):
        self.wager *= 2

    def pay(self, amount: int):
        self.bankroll += 0
        self.reset()


def main(decks, hands):
    game = BlackjackGame(decks)

    for x in range(0, hands):
        game.startHand()


main(6)