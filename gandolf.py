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

    def pickUpNewCardFromDeck(self, deck):                      #pick up card from deck
        return deck[random.randint(0,len(deck) - 1)]

    def swapNewCardWithOld(self, newCard, cards, discardPile):                  #swap card with deck
        x = int(input("which card would you like to swap (1,2,3,4): "))
        discard = cards[x-1]
        cards[x-1] = newCard
        discardPile.append(discard)
    
    def swapMultipleCardsWithTheDeck(self, newCard, cards, discardPile):                  #swap multiple cards with deck
        x = int(input("how many of your cards do you want to swap (2,3,4)"))
        cardsSwapping = []
        cardPosition = []                               
        for i in range(x):
            a = int(input("which card do you want to swap (1,2,3,4)")) -1       
            cardPosition.append(str(a + 1))                                     #stores the position of the cards they want to store
            cardsSwapping.append(int(cards[a][0]))                              #stores the value of the cards

        if round(np.power(np.prod(cardsSwapping), 1/len(cardsSwapping)),10) == float(cards[0][0]):      #checks if all the cards have the same valu by multpilying them all and then finding the nth root using numpy
            for i in range(x):
                discardPile.append(cards[i])                #discards the cards and formats the (virtual)table
                cards[i] = " "
            
            cardPosition = (", ".join(cardPosition))            #gets rid of []
            y = int(input(f"which position would you like to add the new card to {cardPosition}: ")) -1
            cards[y] = newCard
            print(f"you have added the new card to position {y + 1}")           #put the new card in the position requested 
        else:
            p1.mistakeCounter += 5
            print("you have made a mistake")
            print("5 penalty points added")
            print(f"you have {p1.mistakeCounter} penalty points")

    def lookAtOwnCard(self, cards, newCard):
        if newCard[0] == "7" or newCard[0] == "8" :                                        #7/8 - look at own card
            position = int(input("which card would you like to look at (1,2,3,4): "))
            position = position -1
            print(cards[position])
        else:
            p1.mistakeCounter += 5
            print("you have made a mistake")
            print("5 penalty points added")
            print(f"you have {p1.mistakeCounter} penalty points")

    
    def lookAtSomeoneElsesCard(self, newCard):
        if newCard[0] == "9" or newCard[0] == "10":                                                     #9/10 - look at somone elses card
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
            p1.mistakeCounter += 5
            print("you have made a mistake")
            print("5 penalty points added")
            print(f"you have {p1.mistakeCounter} penalty points")

    def swapWithSomoneElse(self,newCard):
        if newCard[0] == "Jack":                                                #jack - swap cards
            ownCard = int(input("which card do you want to swap (1,2,3,4)")) - 1
            playerNumber = int(input("which players card would you like to swap with (2,3,4): "))
            position = int(input("which of their cards would you like swap with (1,2,3,4): ")) - 1
            temp = p1.cards[ownCard]
            if playerNumber == 2:
                p1.cards[ownCard] = p2.cards[position]
                p2.cards[position] = temp
            elif playerNumber == 3:
                p1.cards[ownCard] = p3.cards[position]
                p3.cards[position] = temp
            elif playerNumber == 4:
                p1.cards[ownCard] = p4.cards[position]
                p4.cards[position] = temp
        else:
            p1.mistakeCounter += 5
            print("you have made a mistake")
            print("5 penalty points added")
            print(f"you have {p1.mistakeCounter} penalty points")

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
        if p2[i]== "":
            Vp2[i] = " "
        virtualTable[i+1][0] = Vp2[i]
    for i in range (4):
        if p3[i]== "":
            Vp3[i] = " "
        virtualTable[0][i+1] = Vp3[i]
    for i in range (4):
        if p4[i]== "":
            Vp4[i] = " "
        virtualTable[i+1][5] = Vp4[i] 

    return virtualTable

def displayTable(table):
    for row in table: 
        for elem in row:
            print(elem, end=' ')        # this is how you display 2d arrays
        print()
    

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


table = createTable(table,p1.cards,p2.cards,p3.cards,p4.cards) #create the table with actual cards
displayTable(table)                 #display the table

virtualTable = createVirtualTable(table,p1.cards,p2.cards,p3.cards,p4.cards)        #create the table with virtual cards
displayTable(virtualTable)

Moves = Moves(deck,p1.cards,discardPile)            #this passes in the parameters neccesary for class move - need to look into the theory behind this a bit more
newCard = Moves.pickUpNewCardFromDeck(deck)         #picks random card from deck
print(f"card drawn:", displayCardToPlayer(newCard))                       
option = input(f"would you like to swap cards with {displayCardToPlayer(newCard)}: ")

if option == "yes":
    Moves.swapNewCardWithOld(newCard, p1.cards, discardPile)        #swap cards with deck

option = input("would you like to look at your own card: ")
if option == "yes":
    Moves.lookAtOwnCard(p1.cards, newCard)              #look at own card - 7/8

option = input("would you like to look at someone elses card: ")
if option == "yes":
    Moves.lookAtSomeoneElsesCard(newCard)               #used for showing somone elses card - 9/10

option = input("would you like to swap cards: ")
if option == "yes":
    Moves.swapWithSomoneElse(newCard)                   #swap with soone else - Jack

option = input("would you like to swap multiple cards: ")
if option == "yes":
    Moves.swapMultipleCardsWithTheDeck(newCard, p1.cards, discardPile)  #swap multiple cards with one from deck

print(f"discard pile: {discardPile}")
table = createTable(table,p1.cards,p2.cards,p3.cards,p4.cards) #create the table with actual cards
displayTable(table)
virtualTable = createVirtualTable(table,p1.cards,p2.cards,p3.cards,p4.cards)        #create the table with virtual cards
displayTable(virtualTable)
