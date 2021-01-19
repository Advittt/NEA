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
    def __init__(self,deck,p1,p2,p3,p4,discardPile):
        self.deck = deck
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4
        self.allPlayers = [p1,p2,p3,p4]
        self.discardPile = discardPile

    def pickUpNewCardFromDeck(self, deck):                      #pick up card from deck
        return deck[0]

    def swapNewCardWithOld(self, newCard, cards, discardPile):                  #swap card with deck
        x = int(input("which card would you like to swap (1,2,3,4): "))
        discard = cards[x-1]
        cards[x-1] = newCard
        discardPile.append(discard)
    
    def swapMultipleCardsWithTheDeck(self, newCard, cards, discardPile,counter):                  #swap multiple cards with deck
        x = int(input("how many of your cards do you want to swap (2,3,4)"))
        cardsSwapping = []
        cardPosition = []                               
        for i in range(x):
            a = int(input("which card do you want to swap (1,2,3,4)")) -1       
            cardPosition.append(str(a + 1))                                     #stores the position of the cards they want to store
            if cards[a][0] == "Ace":
                cardsSwapping.append(1)
            elif cards[a][0] == "Jack":
                cardsSwapping.append(11)
            elif cards[a][0] == "Queen":
                cardsSwapping.append(12)
            elif cards[a][0] == "King":
                cardsSwapping.append(12)
            else:      
                cardsSwapping.append(int(cards[a][0]))                              #stores the value of the cards
        if round(np.power(np.prod(cardsSwapping), 1/len(cardsSwapping)),10) == float(cardsSwapping[0]):      #checks if all the cards have the same valu by multpilying them all and then finding the nth root using numpy
            for i in range(x):
                discardPile.append(cards[i])                #discards the cards and formats the (virtual)table
                cards[i] = " "
            
            cardPosition = (", ".join(cardPosition))            #gets rid of []
            y = int(input(f"which position would you like to add the new card to {cardPosition}: ")) -1
            cards[y] = newCard
            print(f"you have added the new card to position {y + 1}")           #put the new card in the position requested 
        else:
            Moves.allPlayers[counter].mistakeCounter += 5
            print("you have made a mistake")
            print("5 penalty points added")
            print(f"you have {Moves.allPlayers[counter].mistakeCounter} penalty points")

    def lookAtOwnCard(self, cards, newCard, counter):
        if newCard[0] == "7" or newCard[0] == "8" :                                        #7/8 - look at own card
            position = int(input("which card would you like to look at (1,2,3,4): "))
            position = position -1
            print(cards[position])
        else:
            Moves.allPlayers[counter].mistakeCounter += 5
            print("you have made a mistake")
            print("5 penalty points added")
            print(f"you have {Moves.allPlayers[counter].mistakeCounter} penalty points")

    
    def lookAtSomeoneElsesCard(self, newCard, counter):
        if newCard[0] == "9" or newCard[0] == "10":                                                     #9/10 - look at somone elses card
            playerNumberList = ["1","2","3","4"]
            playerNumberList.pop(counter)
            playerNumberList = (", ".join(playerNumberList))            #gets rid of []
            playerNumber = int(input(f"which players card would you like to look at {playerNumberList}: "))
            position = int(input("which card would you like to look at (1,2,3,4): ")) -1
            print(Moves.allPlayers[playerNumber -1].cards[position])
        else:
            Moves.allPlayers[counter].mistakeCounter += 5
            print("you have made a mistake")
            print("5 penalty points added")
            print(f"you have {Moves.allPlayers[counter].mistakeCounter} penalty points")

    def swapWithSomoneElse(self,newCard, counter):
        if newCard[0] == "Jack":                                                #jack - swap cards
            playerNumberList = ["1","2","3","4"]
            playerNumberList.pop(counter)
            playerNumberList = (", ".join(playerNumberList))            #gets rid of []
            ownCard = int(input("which card do you want to swap (1,2,3,4)")) - 1
            playerNumber = int(input(f"which players card would you like to swap with {playerNumberList}: "))-1
            position = int(input("which of their cards would you like swap with (1,2,3,4): ")) - 1

            temp = Moves.allPlayers[counter].cards[ownCard]
            Moves.allPlayers[counter].cards[ownCard] = Moves.allPlayers[playerNumber].cards[position]
            Moves.allPlayers[playerNumber].cards[position] = temp

        else:
            Moves.allPlayers[counter].mistakeCounter += 5
            print("you have made a mistake")
            print("5 penalty points added")
            print(f"you have {Moves.allPlayers[counter].mistakeCounter} penalty points")

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
c1 [0] = ["Jack", "Spades"]
c1 [1] = ["Jack", "Hearts"]
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
p4 = Player(4,c4,0,0)



Moves = Moves(deck,p1,p2,p3,p4,discardPile)            #this passes in the parameters neccesary for class move - need to look into the theory behind this a bit more


    
gameActive = True
while gameActive == True:
    for i in range (4):
        print(" \n")
        table = createTable(table,p1.cards,p2.cards,p3.cards,p4.cards) #create the table with actual cards
        displayTable(table)
        virtualTable = createVirtualTable(table,p1.cards,p2.cards,p3.cards,p4.cards)        #create the table with virtual cards
        print(" \n")

        displayTable(virtualTable)
        print(" \n")
        print("**************")
        print(f"PLAYER {i+1} GO:")
        print("**************\n")

        newCard = Moves.pickUpNewCardFromDeck(deck)         #picks random card from deck -- SOMETHIGN BUGGING KEEPS PICKING SAME REPEATED CARDS
        print(f"card drawn:", displayCardToPlayer(newCard))                       
        option = input(f"would you like to swap cards with {displayCardToPlayer(newCard)}: \n")

        done = False
        while done == False:
            no = 0
            if option == "yes":
                Moves.swapNewCardWithOld(newCard, Moves.allPlayers[i].cards, discardPile)        #swap cards with deck
            else:
                no +=1

            option = input("would you like to look at your own card: \n")
            if option == "yes":
                Moves.lookAtOwnCard(Moves.allPlayers[i].cards, newCard,i)              #look at own card - 7/8
            else:
                no +=1

            option = input("would you like to look at someone elses card: \n")
            if option == "yes":
                Moves.lookAtSomeoneElsesCard(newCard,i)               #used for showing somone elses card - 9/10
            else:
                no +=1

            option = input("would you like to swap cards with somone else: \n")
            if option == "yes":
                Moves.swapWithSomoneElse(newCard, i)                   #swap with soone else - Jack
            else:
                no +=1

            option = input("would you like to swap multiple cards: \n")
            if option == "yes":
                Moves.swapMultipleCardsWithTheDeck(newCard, Moves.allPlayers[i].cards, discardPile,i)  #swap multiple cards with one from deck
            else:
                no +=1
            
            if no ==5:
                discardPile.append(newCard)
                deck.pop(0)
            print(f"discard pile: {discardPile}\n")     #DOES NOT SHOW AFTER SWAPPING JACK

            table = createTable(table,p1.cards,p2.cards,p3.cards,p4.cards) #create the table with actual cards
            displayTable(table)
            virtualTable = createVirtualTable(table,p1.cards,p2.cards,p3.cards,p4.cards)        #create the table with virtual cards
            displayTable(virtualTable)

            finished = input("are you done with your go (yes or no)")
            if finished =="yes":
                done = True