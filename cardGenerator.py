import random
from random import shuffle
from collections import deque
class Card:
    def __init__(self, value, color):
        self.value = value
        self.color = color

class Stack:
    def __init__(self):         #deck is now a stack so all you can do is push or pop. first in last out like with normal deck of cards
        self.deck = deque()
    def push(self, card):
        self.deck.append(card)
    def pop(self):
        return self.deck.popleft()
    def peek(self,val):
        return self.deck[val]
    def size(self):
        return len(self.deck)

colors = ['heart', 'diamonds', 'spades', 'clubs']
tempDeck = [Card(value, color) for value in range(1, 14) for color in colors]       #creates a deck of cards in order from all the aces to kings

suits = {1:"Ace", 11: "Jack", 12: "Queen", 13: "King"} 
x = []

deck = Stack()
for i in range(0,52):
    if tempDeck[i].value >= 11 or tempDeck[i].value == 1:                       #if the value is 1 or 11,12,13 then check the dictionary and change suit to ace j,q,k
        value = suits.get(tempDeck[i].value)
        x.append((value, tempDeck[i].color))
    else:
        x.append((str(tempDeck[i].value), tempDeck[i].color))


random.shuffle(x)            # shuffle deck
for i in range (0,52):
    deck.push(x[i])

print(x)