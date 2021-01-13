import random
from random import shuffle
import numpy

class Card:
    def __init__(self, value, color):
        self.value = value
        self.color = color

colors = ['heart', 'diamonds', 'spades', 'clubs']
Deck = [Card(value, color) for value in range(1, 14) for color in colors]

deck = []
for i in range(0,51):
    deck.append((Deck[i].value, Deck[i].color))

random.shuffle(deck)

c1 = [deck[i] for i in range (0,4)]
print(c1[0])

