import random

def randomCard():
    num1 = random.randint(1,13)
    num2 = random.randint(1,4)
    value = ""
    suit = ""

    values = {11: "Jack", 12: "Queen", 13: "King"} 
    value = values.get(num1, num1)
    suits = {1: "Spades", 2: "Hearts", 3: "Diamonds", 4: "Clubs"}       #dictionary for making the deck; uses random to select random cards 
    suit = suits[num2]                                                  #future: change so doesnt pick same random card - there can be duplicates atm - use while loop maybe
    return (value,suit)



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
        return self.deck[random.randint(0,len(self.deck) - 1)]

    def swapNewCardWithOld(self, newCard, cards, discardPile):
        x = int(input("which card would you like to swap (1,2,3,4): "))
        discard = self.cards[x-1]
        self.cards[x-1] = newCard
        self.discardPile.append(discard)

    def lookAtOwnCard(self, cards, newCard):
        if newCard[0] == "7" or newCard[0] == "8" :
            position = int(input("which card would you like to look at (1,2,3,4): "))
            position = position -1
            print(cards[position])
        else:
            print("not 7 or 8")
    
    def lookAtSomeoneElsesCard(self, newCard, player2, player3):
        if newCard[0] == "9" or newCard[0] == "10":
            playerNumber = int(input("which players card would you like to look at (2,3): "))
            position = int(input("which card would you like to look at (1,2,3,4): "))
            position = position -1
            if playerNumber == 2:
                print(p2.cards[position][0])
            elif playerNumber == 3:
                print(p3.cards[position][0])
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
    
rows, cols = (6,6) 
table = [[" " for i in range(cols)] for j in range(rows)]               #table stores the acctual cards and vitural table is what the players see (the back of the card - x)
virtualTable = [[" " for i in range(cols)] for j in range(rows)] 

c1 = [randomCard(),randomCard(),randomCard(),randomCard()]
c2 = [randomCard(),randomCard(),randomCard(),randomCard()]              #selects radnom card
c3 = [randomCard(),randomCard(),randomCard(),randomCard()]
c4 = [randomCard(),randomCard(),randomCard(),randomCard()]

deck = [("7","hearts"),("8","diamonds"),("3","spades"),("2","clubs")]
discardPile = [("3","hearts")]

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


Moves = Moves(deck,Player,discardPile)
print(Moves.cards)
newCard = Moves.pickUpNewCardFromDeck(deck)
print("card drawn:", newCard)
option = input(("would you like to swap cards with:", newCard))
if option == "yes":
    Moves.swapNewCardWithOld(newCard, c1, discardPile)
    print(c1)
    print(discardPile)
Moves.lookAtOwnCard(c1,newCard)
Moves.lookAtSomeoneElsesCard(newCard, p2, p3)
