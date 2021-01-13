import random

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
    


c1 = [("4","hearts"),("4","diamonds"),("4","spades"),("4","clubs")]
c2= [("ace","hearts"),("jack","diamonds"),("queen","spades"),("king", "clubs")]
c3= [("5","hearts"),("5","diamonds"),("5","spades"),("5","clubs")]
deck = [("7","hearts"),("8","diamonds"),("3","spades"),("2","clubs")]

discardPile = [("3","hearts")]
p1 = Player(1,c1,0,0)
p2 = Player(2,c2,0,0)
p3 = Player(3,c3,0,0)



Moves = Moves(deck,c1,discardPile)
newCard = Moves.pickUpNewCardFromDeck(deck)
print("card drawn:", newCard)
option = input(("would you like to swap cards with:", newCard))
if option == "yes":
    Moves.swapNewCardWithOld(newCard, c1, discardPile)
    print(c1)
    print(discardPile)
Moves.lookAtOwnCard(c1,newCard)
Moves.lookAtSomeoneElsesCard(newCard, p2, p3)
