import random
import copy


class Card:
    def __init__(self, suit: str, val: int):
        self.suit = suit
        self.value = val

    def print_value(self):
        if self.value >= 11:
            return 10
        return self.value

    def print_number(self):
        if self.value == 11:
            return "J"
        elif self.value == 12:
            return "Q"
        elif self.value == 13:
            return "K"
        elif self.value == 1:
            return "A"
        else:
            return str(self.value)

    def show(self):
        return "{} of {}".format(self.value, self.suit)


class Deck:
    def __init__(self):
        self.cards = []
        self.pending_shuffle = []
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
        for toShuffle in self.pending_shuffle:
            self.cards.append(toShuffle)
        self.pending_shuffle = copy.deepcopy(self.drawn)
        self.drawn = []
        self.shuffle()

    def check_integrity(self):
        cards = {}
        for card in self.cards:
            if card.show() not in cards:
                cards[card.show()] = 0
            cards[card.show()] += 1
        for card in self.pending_shuffle:
            if card.show() not in cards:
                cards[card.show()] = 0
            cards[card.show()] += 1
        base_count = None
        for key in cards:
            if base_count == None:
                base_count = cards[key]
            elif cards[key] != base_count:
                return False
        return True
