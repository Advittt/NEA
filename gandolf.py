import random
from random import shuffle
import numpy as np
from collections import deque


class Card:
    def __init__(self, value, color):
        self.value = value
        self.color = color

class Stack:
    def __init__(self):         #deck is now a stack so all you can do is push or pop. first in last out
        self.deck = deque()
    def push(self, card):
        self.deck.append(card)
    def pop(self):
        return self.deck.popleft()
    def peek(self,val):
        return self.deck[val]
    def size(self):
        return len(self.deck)

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
        self.allPlayers = [p1,p2,p3,p4]     #use this for selecting players
        self.discardPile = discardPile

    def pickUpNewCardFromDeck(self, deck):                      #pick up card from deck
        newCard = deck.pop()
        return newCard
    
    def pickUpNewCardFromDiscardPile(self, discardPile):                      #pick up card from deck
        newCard = discardPile[0]
        discardPile.pop(0)
        return newCard


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
            print(displayCardToPlayer(cards[position]))
            discardPile.append(newCard)
            newCard = None
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
            print(displayCardToPlayer(Moves.allPlayers[playerNumber -1].cards[position]))
            discardPile.append(newCard)
            newCard = None
        else:
            Moves.allPlayers[counter].mistakeCounter += 5
            print("you have made a mistake")
            print("5 penalty points added")
            print(f"you have {Moves.allPlayers[counter].mistakeCounter} penalty points")

    def swapWithSomoneElse(self,newCard, counter, discardPile):
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
            discardPile.append(newCard)
            newCard = None

        else:
            Moves.allPlayers[counter].mistakeCounter += 5
            print("you have made a mistake")
            print("5 penalty points added")
            print(f"you have {Moves.allPlayers[counter].mistakeCounter} penalty points")

    def skip(self,newCard, counter):
            if newCard[0] == "Queen":                                                #queen - skip go
                discardPile.append(newCard)
                newCard = None
                return True
            else:
                Moves.allPlayers[counter].mistakeCounter += 5
                print("you have made a mistake")
                print("5 penalty points added")
                print(f"you have {Moves.allPlayers[counter].mistakeCounter} penalty points")

    def CheckCommandIsValid(self, Items):
        if Items[0].upper() == "SLAP":
            return "SLAP"
        elif Items[0] == "help":
            return "help"                   
        elif Items[0] == "draw" and (Items[1] == "deck" or Items[1] == "discard"):
            return "draw"
        elif Items[0] == "swap" and (Items[1] == "card" or Items[1] == "cards"):
            return "swap"
        elif Items[0] == "play" and (Items[1] == "7" or Items[1] == "8"):
            return "lookAtOwn"
        elif Items[0] == "play" and (Items[1] == "9" or Items[1] == "10"):
            return "lookAtSomoneElses"
        elif Items[0] == "play" and Items[1] == "jack":
            return "Jack"
        elif Items[0] == "play" and Items[1] == "queen":
            return "Queen"      
        elif Items[0] == "gandalf":
            return "gandalf"
        elif Items[0] == "done":
            return "done"                    
        else:
            return "notValid"
        
    def slapCommand(self, Items):
        print("NEED TO MAKE")
    
    def drawCommand(self, Items,deck,discardPile, chances):
        if chances > 0:
            print("you cannot draw anymore cards for this round")
            print("you can only draw 1 card per turn")
        else:
            if Items[1] == "deck":
                newCard = Moves.pickUpNewCardFromDeck(deck)         #picks random card from deck -- SOMETHIGN BUGGING KEEPS PICKING SAME REPEATED CARDS
            else:
                newCard = Moves.pickUpNewCardFromDiscardPile(discardPile)       #picks random card from discard pile
            print(f"card drawn:", displayCardToPlayer(newCard))             
            return newCard
    def swapCommand(self, Items, newCard, discardPile,i):
        if Items[1] == "card":
            Moves.swapNewCardWithOld(newCard, Moves.allPlayers[i].cards, discardPile)
        else:
            Moves.swapMultipleCardsWithTheDeck(newCard, Moves.allPlayers[i].cards, discardPile,i)

    def gandalfCommand(self, Items):
            print("NEED TO MAKE")

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

def help():
    print("""VALID COMMANDS:
    
1)SLAP
2)draw card deck = draw a card from the deck
3)draw discard = draw a card from the discard
6)swap card = swap one of your cards with the new card drawn
7)swap cards = swap multpile of the same value cards with the new card drawn
8)play 7 = look at one of your own cards
9)play 8 = look at one of your own cards
10)play 9 = look at somone elses card
11)play 10 = look at somone elses card
12)play jack = swap a card with someone else
13)play queen = next player misses a go
14)gandalf = you declare the final round of the game
15)done = finsihed your go
    """)
    
rows, cols = (6,6) 
table = [[" " for i in range(cols)] for j in range(rows)]               #table stores the acctual cards and vitural table is what the players see (the back of the card - x)
virtualTable = [[" " for i in range(cols)] for j in range(rows)] 

colors = ['heart', 'diamonds', 'spades', 'clubs']
tempDeck = [Card(value, color) for value in range(1, 14) for color in colors]       #creates a deck of cards in order from all the aces to kings

suits = {1:"Ace", 11: "Jack", 12: "Queen", 13: "King"} 
x = []
deck = Stack()
for i in range(0,52):
    if tempDeck[i].value >= 11 or tempDeck[i].value == 1:                       #if the vale is 1 or 11,12,13 then check the dictionary and change suit to ace j,q,k
        value = suits.get(tempDeck[i].value)
        x.append((value, tempDeck[i].color))
    else:
        x.append((str(tempDeck[i].value), tempDeck[i].color))


random.shuffle(x)            # shuffle deck
for i in range (0,52):
    deck.push(x[i])

c1 = []
c2 = []
c3 = []
c4 = []
for i in range (0,4):
    c1.append(deck.peek(i))
    deck.pop()
    c2.append(deck.peek(i))
    deck.pop()
    c3.append(deck.peek(i))
    deck.pop()
    c4.append(deck.peek(i))
    deck.pop()

discardPile = []
p1 = Player(1,c1,0,0)
p2 = Player(2,c2,0,0)
p3 = Player(3,c3,0,0)
p4 = Player(4,c4,0,0)

Moves = Moves(deck,p1,p2,p3,p4,discardPile)            #this passes in the parameters neccesary for class move - need to look into the theory behind this a bit more

skip = False            # for queen
Gandalf = False
while Gandalf == False:
    for i in range (4):
        if skip == False:
            print(" \n")
            table = createTable(table,p1.cards,p2.cards,p3.cards,p4.cards) #create the table with actual cards
            displayTable(table)
            virtualTable = createVirtualTable(table,p1.cards,p2.cards,p3.cards,p4.cards)        #create the table with virtual cards
            print(" \n")

            displayTable(virtualTable)
            print(" \n")
            print("**************")
            print(f"PLAYER {i+1}'S GO:")
            print("**************\n")
            drawACardChances = 0
            done = False
            while done == False:

                Commands = []
                Commands.append(input(f"Enter command: ").lower())
                for C in Commands:
                    Items = []                                      #splits commands up
                    Items = C.split(" ")
                ValidCommand = Moves.CheckCommandIsValid(Items)        #check if valid 
                if ValidCommand == "notValid":
                    print("Invalid command")
                elif ValidCommand == "SLAP":
                    Moves.slapCommand(Items)
                elif ValidCommand == "help":
                    help()
                elif ValidCommand == "draw":
                    newCard = Moves.drawCommand(Items,deck,discardPile,drawACardChances)        #draw card
                    drawACardChances += 1
                elif ValidCommand == "swap":
                    Moves.swapCommand(Items,newCard, discardPile,i)
                    table = createTable(table,p1.cards,p2.cards,p3.cards,p4.cards) #create the table with actual cards
                    displayTable(table)
                    virtualTable = createVirtualTable(table,p1.cards,p2.cards,p3.cards,p4.cards)        #create the table with virtual cards
                    displayTable(virtualTable)   
                elif ValidCommand == "lookAtOwn":
                    Moves.lookAtOwnCard(Moves.allPlayers[i].cards, newCard,i)              #look at own card - 7/8 
                elif ValidCommand == "lookAtSomoneElses":
                    Moves.lookAtSomeoneElsesCard(newCard,i)               #used for showing somone elses card - 9/10
                elif ValidCommand == "Jack":
                    Moves.swapWithSomoneElse(newCard, i, discardPile)                   #swap with soone else - Jack
                    table = createTable(table,p1.cards,p2.cards,p3.cards,p4.cards) #create the table with actual cards
                    displayTable(table)
                    virtualTable = createVirtualTable(table,p1.cards,p2.cards,p3.cards,p4.cards)        #create the table with virtual cards
                    displayTable(virtualTable)
                elif ValidCommand == "Queen":
                    skip = Moves.skip(newCard, i)                   #skip a go - Queen
                elif ValidCommand == "done":
                    done = True             #go finished
                    print("TABLE AT END OF TURN")
                    table = createTable(table,p1.cards,p2.cards,p3.cards,p4.cards) #create the table with actual cards
                    displayTable(table)
                    virtualTable = createVirtualTable(table,p1.cards,p2.cards,p3.cards,p4.cards)        #create the table with virtual cards
                    displayTable(virtualTable)
                    discardPile.reverse()       #correct the order
                    print(f"discard pile: {discardPile[0]}")                   
                Commands.clear()

        else:
            print(f"***PLAYER {Moves.allPlayers[i].playerNumber} MISSES A GO***")
            skip = False    #if queen is used to skip then when its the next players turn it will skip the whole code and go to he next players turn
            done = True
        