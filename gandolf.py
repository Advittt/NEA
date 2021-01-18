import random
from random import shuffle
import numpy as np

class Card:
    def __init__(self, value, color):
        self.value = value
        self.color = color

class Player:
    def __init__(self, playerNumber, cards, totalPoints, mistakeCounter):
        self.playerNumber = playerNumber
        self.cards = cards
        self.totalPoints = totalPoints
        self.mistakeCounter = mistakeCounter

class Moves:
    def __init__(self,deck,cards,discardPile):
        self.deck = deck
        self.cards = cards
        self.discardPile = discardPile

    def pickUpNewCardFromDeck(self, deck):
        return deck[random.randint(0,len(deck) - 1)]

    def swapNewCardWithOld(self, newCard, cards, discardPile):
        x = int(input("which card would you like to swap (1,2,3,4): "))
        discard = cards[x-1]
        cards[x-1] = newCard
        discardPile.append(discard)

    def lookAtOwnCard(self, cards, newCard):
        if newCard[0] == "7" or newCard[0] == "8" :
            position = int(input("which card would you like to look at (1,2,3,4): "))
            position = position -1
            print(cards[position])
        else:
            print("not 7 or 8")
    
    def lookAtSomeoneElsesCard(self, newCard, player2, player3, player4):
        if newCard[0] == "9" or newCard[0] == "10":
            playerNumber = int(input("which players card would you like to look at (2,3,4): "))
            position = int(input("which card would you like to look at (1,2,3,4): "))
            position = position -1
            if playerNumber == 2:
                print(p2.cards[position])
            elif playerNumber == 3:
                print(p3.cards[position])
            elif playerNumber == 4:
                print(p4.cards[position])
        else:
            print("not 9 or 10")

def createTable(table,p1,p2,p3,p4):         #creates table to store actual values of cards nd positions
    for i in range (4):
        table[5][i+1] = p1[i]
    for i in range (4):
        table[i+1][0] = p2[i]
    for i in range (4):
        table[0][i+1] = p3[i]
    for i in range (4):
        table[i+1][5] = p4[i]
    return(table)

def createVirtualTable(table,p1,p2,p3,p4):      #creates virutal table with just x's which is displayed to  players 
    Vp1 = ["x"] * 4
    Vp2 = ["x"] * 4
    Vp3 = ["x"] * 4
    Vp4 = ["x"] * 4

    for i in range (4):
        if p1[i]== " ":                     #if there is no longer a card in that place it, it will show as a gap in the terminal
            Vp1[i] = " "
        virtualTable[5][i+1] = Vp1[i]           
    for i in range (4):
        if p2[i]== " ":
            Vp2[i] = " "
        virtualTable[i+1][0] = Vp2[i]
    for i in range (4):
        if p3[i]== " ":
            Vp3[i] = " "
        virtualTable[0][i+1] = Vp3[i]
    for i in range (4):
        if p4[i]== " ":
            Vp4[i] = " "
        virtualTable[i+1][5] = Vp4[i] 

    return virtualTable

def displayCardToPlayer(card):
    return (f"the {card[0]} of {card[1]}")          #displays cards in user readable/friendly way 
    
rows, cols = (6,6) 
table = [[" " for i in range(cols)] for j in range(rows)]               #table stores the acctual cards and vitural table is what the players see (the back of the card - x)
virtualTable = [[" " for i in range(cols)] for j in range(rows)] 

colors = ['heart', 'diamonds', 'spades', 'clubs']
Deck = [Card(value, color) for value in range(1, 14) for color in colors]       #creates a deck of cards in order from all the aces to kings

deck = []
suits = {1:"Ace", 11: "Jack", 12: "Queen", 13: "King"} 

for i in range(0,52):
    if Deck[i].value >= 11 or Deck[i].value == 1:                       #if the vale is 1 or 11,12,13 then check the dictionary and change suit to ace j,q,k
        value = suits.get(Deck[i].value)
        deck.append([value, Deck[i].color])
    else:
        deck.append([str(Deck[i].value), Deck[i].color])


random.shuffle(deck)            # shuffle deck

c1 = ([deck[i] for i in range (0,4)])
deck = deck[4:]                                 #deals cards - takes first 4 cards from the deck and then removes the cards from the deck 
c2 = ([deck[i] for i in range (0,4)])
deck = deck[4:]
c3 = ([deck[i] for i in range (0,4)])
deck = deck[4:]
c4 = ([deck[i] for i in range (0,4)])
deck = deck[4:]

discardPile = []

p1 = Player(1,c1,0,0)
p2 = Player(2,c2,0,0)
p3 = Player(3,c3,0,0)
p4 = Player(3,c4,0,0)


table = createTable(table,p1.cards,p2.cards,p3.cards,p4.cards)
for row in table: 
    for elem in row:
        print(elem, end=' ')        # this is how you display 2d arrays
    print()

for row in createVirtualTable(table,p1.cards,p2.cards,p3.cards,p4.cards):
    for elem in row:
        print(elem, end=' ')
    print()

Moves = Moves(deck,p1.cards,discardPile)            #this passes in the parameters neccesary for class move - need to look into the theory behind this a bit more
newCard = Moves.pickUpNewCardFromDeck(deck)         #picks random card from deck
print(f"card drawn:", displayCardToPlayer(newCard))                       
option = input(f"would you like to swap cards with {displayCardToPlayer(newCard)}: ")

if option == "yes":
    Moves.swapNewCardWithOld(newCard, p1.cards, discardPile)        #swap cards with deck
    print(p1.cards)
    print(discardPile)                                              #just shows it worked
Moves.lookAtOwnCard(p1.cards,newCard)
Moves.lookAtSomeoneElsesCard(newCard, p2, p3, p4)               #used for showing somone elses card