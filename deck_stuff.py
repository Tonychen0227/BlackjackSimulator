import random


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

