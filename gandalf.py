import random
from random import shuffle
import numpy as np
from collections import deque
import time

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


class Player:               #parent class for humans
    def __init__(self, playerNumber, cards, totalPoints, mistakeCounter,difficulty):
        self.playerNumber = playerNumber
        self.cards = cards
        self.totalPoints = totalPoints
        self.mistakeCounter = mistakeCounter
        self.difficulty = difficulty

class AIPlayer(Player):         # AI child class
    def __init__(self, playerNumber, cards, totalPoints, mistakeCounter, difficulty, playersCardsDictionary):
        super().__init__(playerNumber, cards, totalPoints, mistakeCounter,difficulty)
        self.playersCardsDictionary = playersCardsDictionary

    
class Moves:
    def __init__(self,deck,p1,p2,p3,p4,discardPile):
        self.deck = deck
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4
        self.allPlayers = [p1,p2,p3,p4]     #use this for selecting players
        self.discardPile = discardPile
    
    def lookAtCardsStartofRound(self, cards, card1, card2):
        return[(cards[card1]),(cards[card2])]
        
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
        cardsSwapping = []              #cardsSwapping holds the value of the card and cardsSwapping1 holds the card as tuple
        cardsSwapping1 = []
        cardPosition = []           #cardPosition holds the postion of the players cards as a string and cardPosition1 as an integer
        cardPosition1 = []                                
        for i in range(x):
            a = int(input("which card do you want to swap (1,2,3,4)")) -1       
            cardPosition.append(str(a + 1))                                     #stores the position of the cards they want to store
            cardPosition1.append(a)
            if cards[a][0] == "Ace":
                cardsSwapping1.append(("Ace",cards[a][1]))          #convert AJQK into its number value and store in list cardsSwapping. the tuple itself is stored in cardsSwapping1
                cardsSwapping.append(1)
            elif cards[a][0] == "Jack":
                cardsSwapping.append(11)
                cardsSwapping1.append(("Jack",cards[a][1]))
            elif cards[a][0] == "Queen":
                cardsSwapping.append(12)
                cardsSwapping1.append(("Queen",cards[a][1]))
            elif cards[a][0] == "King":
                cardsSwapping.append(13)
                cardsSwapping1.append(("King",cards[a][1]))
            else:
                cardsSwapping.append(int(cards[a][0]))       
                cardsSwapping1.append([int(cards[a][0]),cards[a][1]])                             #stores the value of the cards
        if round(np.power(np.prod(cardsSwapping), 1/len(cardsSwapping)),10) == float(cardsSwapping[0]):      #checks if all the cards have the same value by multpilying them all and then finding the nth root using numpy
            for i in range (x):
                Moves.discard(discardPile, cardsSwapping1[i]) #discard the players card
            for j in cardPosition1:
                cards[j] = " "              #remove players card from their hand
            
            cardPosition = (", ".join(cardPosition))            #gets rid of []
            y = int(input(f"which position would you like to add the new card to {cardPosition}: ")) -1
            Moves.allPlayers[counter].cards[y] = newCard
            print(f"you have added the new card to position {y + 1}")           #put the new card in the position requested 

        else:
            Moves.allPlayers[counter].mistakeCounter += 5
            print("you have made a mistake")
            print("5 penalty points added")
            print(f"you have {Moves.allPlayers[counter].mistakeCounter} penalty points")
    
    

    def lookAtOwnCard(self, cards, newCard, counter, playerDifficulty, AIChoice):
        if playerDifficulty == 0:                   #check if you are a human or AI
            if newCard[0] == "7" or newCard[0] == "8" :                                        #7/8 - look at own card
                position = int(input("which card would you like to look at (1,2,3,4): "))
                position = position -1
                print(displayCardToPlayer(cards[position]))
                discardPile.append(newCard)
                return (None,None)
            else:
                Moves.allPlayers[counter].mistakeCounter += 5
                print("you have made a mistake")
                print("5 penalty points added")
                print(f"you have {Moves.allPlayers[counter].mistakeCounter} penalty points")
        else:
            discardPile.append(newCard)
            return Moves.allPlayers[counter].cards[AIChoice]


    
    def lookAtSomeoneElsesCard(self, newCard, playerDifficulty, playerNumber, counter):
        if playerDifficulty == 0:
            if newCard[0] == "9" or newCard[0] == "10":                                                     #9/10 - look at somone elses card
                playerNumberList = ["1","2","3","4"]
                playerNumberList.pop(counter)
                playerNumberList = (", ".join(playerNumberList))            #gets rid of []
                playerNumber = int(input(f"which players card would you like to look at {playerNumberList}: "))
                position = int(input("which card would you like to look at (1,2,3,4): ")) -1
                print(displayCardToPlayer(Moves.allPlayers[playerNumber -1].cards[position]))
                discardPile.append(newCard)
                return (None,None)
            else:
                Moves.allPlayers[counter].mistakeCounter += 5
                print("you have made a mistake")
                print("5 penalty points added")
                print(f"you have {Moves.allPlayers[counter].mistakeCounter} penalty points")
        else:
            discardPile.append(newCard)     #AIs version
            playerNumberList = [1,2,3,4]
            playerNumberList.pop(counter)
            playerNumber = random.choice(playerNumberList)
            position = random.randint(0,3)
            return([playerNumber, position, Moves.allPlayers[playerNumber -1].cards[position]])            

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
            return (None,None)

        else:
            Moves.allPlayers[counter].mistakeCounter += 5
            print("you have made a mistake")
            print("5 penalty points added")
            print(f"you have {Moves.allPlayers[counter].mistakeCounter} penalty points")

    def skip(self,newCard):
            if newCard[0] == "Queen":                                                #queen - skip go # AI share this method
                discardPile.append(newCard)
                return True, (None,None)
            else:
                Moves.allPlayers[counter].mistakeCounter += 5
                print("you have made a mistake")
                print("5 penalty points added")
                print(f"you have {Moves.allPlayers[counter].mistakeCounter} penalty points")
    
    def drawCommand(self, Items,deck,discardPile, chances):
        if chances > 0:
            print("you cannot draw anymore cards for this round")
            print("you can only draw 1 card per turn")
        else:
            if Items[1] == "deck":
                newCard = Moves.pickUpNewCardFromDeck(deck)         #picks random card from deck
            else:
                newCard = Moves.pickUpNewCardFromDiscardPile(discardPile)       #picks random card from discard pile
            print(f"card drawn:", displayCardToPlayer(newCard))             
            return newCard

    def discard(self,discardPile,newCard):  #adds new card to discardPile
        discardPile.append(newCard)
        return (None,None)

    def newCardUsed(self,newCard):  #check if new card has already been used. stops repeating turns
        if newCard[0] == None:
            return True
        else:
            return False

    def swapCommand(self, Items, newCard, discardPile,i):
        if Items[1] == "card":
            Moves.swapNewCardWithOld(newCard, Moves.allPlayers[i].cards, discardPile)
        else:
            Moves.swapMultipleCardsWithTheDeck(newCard, Moves.allPlayers[i].cards, discardPile,i)

    def gandalfCommand(self, allowed):
        if allowed == 0:    #if this is their first command, then they can call gandalf
            return True
        else:
            return False

    def help():
        print("""VALID COMMANDS:
            
        1)draw deck = draw a card from the deck
        2)draw discard = draw a card from the discard
        3)swap card = swap one of your cards with the new card drawn
        4)swap cards = swap multpile of the same value cards with the new card drawn
        5)play 7 = look at one of your own cards
        6)play 8 = look at one of your own cards
        7)play 9 = look at somone elses card
        8)play 10 = look at somone elses card
        9)play jack = swap a card with someone else
        10)play queen = next player misses a go
        11)gandalf = you declare the final round of the game
        12)done = finsihed your go
        13) quit
        14) save
            """)
    
    def CheckCommandIsValid(self, Items):
        if Items[0] == "help":
            return "help"                   
        elif Items[0] == "draw" and (Items[1] == "deck" or Items[1] == "discard"):
            return "draw"
        elif Items[0] == "discard":
            return "discard"
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
        elif Items[0] == "quit":
            return "quit"
        elif Items[0] == "save":
            return "save"                 
        else:
            return "notValid"




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

def displayTable(table):
    for row in table: 
        for elem in row:
            print(elem, end=' ')        # this is how you display 2d arrays
        print()



def displayCardToPlayer(card):
    return (f"the {card[0]} of {card[1]}")          #displays cards in user readable/friendly way


def merge(left, right):     #merge sort algorithm with reccursion. this is used for sorting out the tuples and 2d arrays from lowest to highest
        left_index, right_index = 0, 0
        result = []
        while left_index < len(left) and right_index < len(right):
            if left[left_index] < right[right_index]:
                result.append(left[left_index])
                left_index += 1
            else:
                result.append(right[right_index])
                right_index += 1

        result += left[left_index:]
        result += right[right_index:]
        return result


def merge_sort(array):
    if len(array) <= 1:  
        return array

    # divide array in half and merge sort recursively
    half = len(array) // 2
    left = merge_sort(array[:half])
    right = merge_sort(array[half:])

    return merge(left, right)


def main(Moves,discardPile,Card,Stack,Player,table,virtualTable,preSetDifficulty):
    skip = False            # for queen
    Gandalf = False
    if preSetDifficulty == False:
        for d in range (3):                                                                                     #set AI player difficulties
            D = input(f"""what difficulty do you want player {Moves.allPlayers[d].playerNumber + 1} to have:
            1 = easy
            2 = medium
            3 = hard
            """)
            Moves.allPlayers[d+1].difficulty = D
            print(f"player {Moves.allPlayers[d].playerNumber+ 1} is set to {D} difficulty")
    Round = 0
    while Gandalf == False:
        Round = Round +1
        for i in range (4):
            if skip == False:        
                print(" \n")
                table = createTable(table,p1.cards,p2.cards,p3.cards,p4.cards)  #create the table with actual cards
                #displayTable(table)
                virtualTable = createVirtualTable(table,p1.cards,p2.cards,p3.cards,p4.cards)        #create the table with virtual cards
                print(" \n")

                displayTable(virtualTable)
                print(" \n")
                print("**************")
                print(f"PLAYER {i+1}'S GO:")
                print("**************\n")
                callGandalfChecker = 0
                drawACardChances = 0
                done = False
                duringRound = 0
                allowSaveGame = 0
                newCard = (None,None)
                while done == False:
                    duringRound = duringRound + 1
                    while i == 0:
                        allowSaveGame = allowSaveGame + 1
                        if Round == 1 and duringRound == 1:
                            a = int(input("which cards would you like to look at: 1,2,3 or 4")) -1
                            b = int(input("which cards would you like to look at: 1,2,3 or 4")) -1
                            cardsChosen = Moves.lookAtCardsStartofRound(Moves.allPlayers[i].cards,a,b)
                            print(displayCardToPlayer(cardsChosen[0]))
                            print(displayCardToPlayer(cardsChosen[1]))
                        duringRound = duringRound + 1

                        Commands = []
                        Commands.append(input(f"Enter command: ").lower())
                        for C in Commands:
                            Items = []                                      #splits commands up
                            Items = C.split(" ")
                        ValidCommand = Moves.CheckCommandIsValid(Items)        #check if valid 

                        if ValidCommand == "notValid":
                            print("Invalid command")

                        

                        elif ValidCommand == "help":
                            help()

                        elif ValidCommand == "draw":
                            newCard = Moves.drawCommand(Items,deck,discardPile,drawACardChances)        #draw card
                            drawACardChances += 1
                            callGandalfChecker += 1

                        elif ValidCommand == "discard":
                            if Moves.newCardUsed(newCard) == False:                 #if the new card has already been used, dont do the following command
                                newCard = Moves.discard(discardPile, newCard)        #e.g. do not append (Non,None to discardPile)#discard card drawn
                                drawACardChances += 1                               
                                callGandalfChecker += 1
                            else:
                                print("you have already used your card")

                        elif ValidCommand == "swap":
                            if Moves.newCardUsed(newCard) == False:
                                Moves.swapCommand(Items,newCard, discardPile,i)
                                table = createTable(table,p1.cards,p2.cards,p3.cards,p4.cards) #create the table with actual cards
                                #displayTable(table)
                                virtualTable = createVirtualTable(table,p1.cards,p2.cards,p3.cards,p4.cards)        #create the table with virtual cards
                                displayTable(virtualTable)
                                callGandalfChecker += 1
                            else:
                                print("you have already used your card")

                        elif ValidCommand == "lookAtOwn":
                            if Moves.newCardUsed(newCard) == False:
                                newCard = Moves.lookAtOwnCard(Moves.allPlayers[i].cards, newCard,i, Moves.allPlayers[i].difficulty,0)              #look at own card - 7/8 
                                callGandalfChecker += 1
                            else:
                                print("you have already used your card")


                        elif ValidCommand == "lookAtSomoneElses":
                            if Moves.newCardUsed(newCard) == False:
                                newCard = Moves.lookAtSomeoneElsesCard(newCard, Moves.allPlayers[i].difficulty, Moves.allPlayers[i].playerNumber,i)               #used for showing somone elses card - 9/10
                                callGandalfChecker += 1
                            else:
                                print("you have already used your card")


                        elif ValidCommand == "Jack":
                            if Moves.newCardUsed(newCard) == False:
                                newCard = Moves.swapWithSomoneElse(newCard, i, discardPile)                   #swap with soone else - Jack
                                table = createTable(table,p1.cards,p2.cards,p3.cards,p4.cards) #create the table with actual cards
                                #displayTable(table)
                                virtualTable = createVirtualTable(table,p1.cards,p2.cards,p3.cards,p4.cards)        #create the table with virtual cards
                                displayTable(virtualTable)
                                callGandalfChecker += 1
                            else:
                                print("you have already used your card")

                        elif ValidCommand == "Queen": 
                            if Moves.newCardUsed(newCard) == False:
                                a = Moves.skip(newCard)                   #skip a go - Queen
                                skip = a[0]
                                newCard = a[1]
                                callGandalfChecker += 1
                            else:
                                print("you have already used your card")

                        elif ValidCommand == "gandalf":
                            Gandalf = Moves.gandalfCommand(callGandalfChecker)                   #Gandalf - end game
                            if Gandalf == True:
                                done = True             #go finished
                                i = 5
                                print("TABLE AT END OF TURN")
                                table = createTable(table,p1.cards,p2.cards,p3.cards,p4.cards) #create the table with actual cards
                                #displayTable(table)
                                virtualTable = createVirtualTable(table,p1.cards,p2.cards,p3.cards,p4.cards)        #create the table with virtual cards
                                displayTable(virtualTable)
                                if len(discardPile) !=0:
                                    print(f"discard pile: {discardPile[len(discardPile) -1]}")  
                                Commands.clear()
                            else:
                                print("cannot call gandalf")
                                print("you can only call gandalf at the beginning of your round")

                        elif ValidCommand == "done":
                            if Moves.newCardUsed(newCard) == False:         #if they have not used their card yet, then disard it for them
                                Moves.discard(discardPile, newCard)
                            done = True             #go finished
                            i = 5
                            print("TABLE AT END OF TURN")
                            table = createTable(table,p1.cards,p2.cards,p3.cards,p4.cards) #create the table with actual cards
                            #displayTable(table)
                            virtualTable = createVirtualTable(table,p1.cards,p2.cards,p3.cards,p4.cards)        #create the table with virtual cards
                            displayTable(virtualTable)
                            if len(discardPile) !=0:
                                print(f"discard pile: {discardPile[len(discardPile) -1]}")

                        elif ValidCommand == "quit":
                            confirm = input("you have not saved this game yet. are you sure you want to quit the game? ")
                            if confirm == "yes":
                                print("you have chosen to quit the game. goodbye")
                                break
                            else:
                                pass

                        elif ValidCommand == "save":
                            if allowSaveGame == 1:
                                newGameFileName = input("what do you want to save the game file as: ")
                                f = open(f"{newGameFileName}.txt", "w")
                                formatDeck = [] 
                                for i in range (deck.size()):
                                    formatDeck.append(deck.peek(i))
                                f.write(str(formatDeck))
                                f.write("\n")
                                f.write(str(discardPile))
                                f.write("\n")
                                f.write(str(p1.cards))
                                f.write("\n")
                                f.write(str(p2.cards))
                                f.write("\n")
                                f.write(str(p3.cards))
                                f.write("\n")
                                f.write(str(p4.cards))
                                f.write("\n")
                                f.write(str(p1.mistakeCounter))
                                f.write("\n")
                                f.write(str(p2.mistakeCounter))
                                f.write("\n")
                                f.write(str(p3.mistakeCounter))
                                f.write("\n")
                                f.write(str(p4.mistakeCounter))
                                f.write("\n")
                                f.write(str(p2.difficulty))
                                f.write("\n")
                                f.write(str(p3.difficulty))
                                f.write("\n")
                                f.write(str(p4.difficulty))
                                f.write("\n")
                                f.write(str(p2.playersCardsDictionary))
                                f.write("\n")
                                f.write(str(p3.playersCardsDictionary))
                                f.write("\n")
                                f.write(str(p4.playersCardsDictionary))
                                f.close()          

                                print("the game has been saved. Goodbye")
                                break
                            else:
                                print("you can only save the game at the start of your go")      
                        Commands.clear()

                    
                    while i == 1:          #player 2 AI
                        difficulty = Moves.allPlayers[i].difficulty
                        probability = random.randint(1,10)
                        forget = random.randint(1,100)
                        percentage = 0
                        if difficulty == 1:
                            percentage = 50
                        elif difficulty == 2:
                            percentage = 70
                        elif difficulty == 3:
                            percentage = 90
                                    
                        if Round == 1:
                            temp = Moves.lookAtCardsStartofRound(p2.cards,0,1)
                            knownCards = [list(temp[0]),list(temp[1])]
                            knownCards.append([None,None])
                            knownCards.append([None,None])
                        tempCards = []
                        Items = ["draw","deck"]
                        drawACardChances = 0

                        cardValue = []
                        for j in p2.cards:
                            if j[0] == "Ace":
                                cardValue.append(1)
                            elif j[0] == "Jack":
                                cardValue.append(11)
                            elif j[0] == "Queen":
                                cardValue.append(12)
                            elif j[0] == "King":
                                cardValue.append(13)
                            else:
                                cardValue.append(int(j[0]))
                        
                        if sum(cardValue) <= 5:
                            print(f"PLAYER {Moves.allPlayers[i].playerNumber} HAS SAID GANDALF!")
                            print("FINAL ROUND")
                            Gandalf = True
                            done = True             #go finished
                            i = 5
                            print("TABLE AT END OF TURN")
                            table = createTable(table,p1.cards,p2.cards,p3.cards,p4.cards) #create the table with actual cards
                            #displayTable(table)
                            virtualTable = createVirtualTable(table,p1.cards,p2.cards,p3.cards,p4.cards)        #create the table with virtual cards
                            displayTable(virtualTable)
                            if len(discardPile) !=0:
                                print(f"discard pile: {discardPile[len(discardPile) -1]}")  

                        newCard = Moves.drawCommand(Items,deck,discardPile,drawACardChances)        #draw card
                        time.sleep(5)

                        if newCard[0] == "7" or newCard[0] == "8":          #play 7 or 8
                            seenCard = Moves.lookAtOwnCard(p2.cards, newCard, i, p2.playerNumber, 2)
                            knownCards.append(seenCard)
                            newCard = (None,None)
                            time.sleep(5)

                        
                        elif newCard[0] == "9" or newCard[0] == "10":       #play 9 or 10
                            print(f"PLAYER {Moves.allPlayers[i].playerNumber} HAS PLAYED A {newCard[0]}")
                            listOfCards = Moves.lookAtSomeoneElsesCard(newCard, Moves.allPlayers[i].difficulty, Moves.allPlayers[i].playerNumber, i)
                            playerNumber = listOfCards[0]
                            position = listOfCards[1]
                            playerCard = listOfCards[2]

                            if playerNumber == 1:
                                playerNumber = "player1"
                            elif playerNumber == 3:
                                playerNumber = "player3"
                            elif playerNumber == 4:
                                playerNumber = "player4"
                            if position == 0:
                                position = "card1"
                            elif position == 1:
                                position = "card2"
                            elif position == 2:
                                position = "card3"
                            else:
                                position = "card4"

                            if percentage == 50:
                                if 1 <= probability and probability <= 5:
                                    if forget <= 10:
                                        Moves.allPlayers[i].playersCardsDictionary["players"][playerNumber][position] = deck.peek(0)
                                    else:
                                        Moves.allPlayers[i].playersCardsDictionary["players"][playerNumber][position] = playerCard
                            elif percentage == 70:
                                if 1 <= probability and probability <= 7:
                                    if forget <= 6:
                                        Moves.allPlayers[i].playersCardsDictionary["players"][playerNumber][position] = deck.peek(0)
                                    else:
                                        Moves.allPlayers[i].playersCardsDictionary["players"][playerNumber][position] = playerCard
                            else:
                                if 1 <= probability and probability <= 9:
                                    if forget == 1:
                                        Moves.allPlayers[i].playersCardsDictionary["players"][playerNumber][position] = deck.peek(0)
                                    else:
                                        Moves.allPlayers[i].playersCardsDictionary["players"][playerNumber][position] = playerCard

                            print(f"player {Moves.allPlayers[i].playerNumber} has seen {playerNumber}'s {position} ")

                            time.sleep(5)

                        elif newCard[0] == "Jack":       
                            playersCardsValue = []
                            for key in Moves.allPlayers[1].playersCardsDictionary["players"].keys():
                                x =1
                                for value in Moves.allPlayers[1].playersCardsDictionary["players"][key].values():
                                    value = [value[0],value[1]]
                                    if value == [None,None]:
                                        pass
                                        x = x+1
                                    else:
                                        if value[0]== "Ace":
                                            value[0]= 1
                                        elif value[0]== "Jack":
                                            value[0] = 11
                                        elif value[0]== "Queen":
                                            value[0] = 12
                                        elif value[0]== "King":
                                            value[0] = 13
                                        else:
                                            value[0]= int(value[0])
                                        playersCardsValue.append([value[0],value[1],key,x])   #card value, card suit, playernumber, card position
                                        x = x+1

                            playersCardsValue = merge_sort(playersCardsValue)

                            sortedKnownCards = []
                            for val in range(len(knownCards)):
                                Rval = 0
                                if knownCards[val][0]== "Ace":
                                    Rval= 1
                                elif knownCards[val][0]== "Jack":
                                    Rval = 11
                                elif knownCards[val][0]== "Queen":
                                    Rval= 12
                                elif knownCards[val][0]== "King":
                                    Rval= 13
                                elif knownCards[val][0]== None:
                                    Rval= 0
                                else:
                                    Rval= int(knownCards[val][0])
                                sortedKnownCards.append([Rval,knownCards[val][1],val]) #card value, card suit, card position
                            sortedKnownCards = merge_sort(sortedKnownCards)

                            playerNumberList = [0,2,3]
                            playerNumber = playerNumberList[random.randint(0,2)]
                            playerNumbersCardPosition = random.randint(0,3)
                            
                            rememebers = False

                            if percentage == 50:
                                if 1 <= probability and probability <= 5:
                                    temporaryCard = p2.cards[0]
                                    p2.cards[0] = Moves.allPlayers[playerNumberList[playerNumber]].cards[playerNumbersCardPosition]
                                    Moves.allPlayers[playerNumberList[playerNumber]].cards[playerNumbersCardPosition] = temporaryCard
                                    print(f"player {Moves.allPlayers[i].playerNumber} swapped cards with player {playerNumber + 1}'s card {playerNumbersCardPosition}")
                                else:
                                    rememebers = True 
                            elif percentage == 70:
                                if 1 <= probability and probability <= 3:
                                    temporaryCard = p2.cards[0]
                                    p2.cards[0] = Moves.allPlayers[playerNumberList[playerNumber]].cards[playerNumbersCardPosition]
                                    Moves.allPlayers[playerNumberList[playerNumber]].cards[playerNumbersCardPosition] = temporaryCard 
                                    print(f"player {Moves.allPlayers[i].playerNumber} swapped cards with player {playerNumber + 1}'s card {playerNumbersCardPosition}")
                                else:
                                    rememebers = True 
                            else:
                                if 1 == probability:
                                    temporaryCard = p2.cards[0]
                                    p2.cards[0] = Moves.allPlayers[playerNumberList[playerNumber]].cards[playerNumbersCardPosition]
                                    Moves.allPlayers[playerNumberList[playerNumber]].cards[playerNumbersCardPosition] = temporaryCard 
                                    print(f"player {Moves.allPlayers[i].playerNumber} swapped cards with player {playerNumber + 1}'s card {playerNumbersCardPosition}")
                                else:
                                    rememebers = True 

                            if rememebers == True:

                                if len(playersCardsValue) == 0:
                                    pass
                                elif sortedKnownCards[3][0] > playersCardsValue[0][0]:      #swaps AI players highest card with the known lowest card
                                    tempKnownCard = list(sortedKnownCards[3])
                                    tempPlayersCardsValue = list(playersCardsValue[0])

                                    sortedKnownCards[3][0] = tempPlayersCardsValue[0]
                                    sortedKnownCards[3][1] = tempPlayersCardsValue[1]

                                    playersCardsValue[0][0]= tempKnownCard[0]
                                    playersCardsValue[0][1]= tempKnownCard[1]
                                    print(playersCardsValue)
                                    if playersCardsValue[0][0]== 1:
                                        playersCardsValue[0][0] = "Ace"
                                    elif playersCardsValue[0][0]== 11:
                                        playersCardsValue[0][0] = "Jack"
                                    elif playersCardsValue[0][0]== 12:
                                        playersCardsValue[0][0] = "Queen"
                                    elif playersCardsValue[0][0]== 13:
                                        playersCardsValue[0][0] = "King"
                                    else:
                                        pass
                                    if sortedKnownCards[3][0]== 1:
                                        sortedKnownCards[3][0] = "Ace"
                                    elif psortedKnownCards[3][0]== 11:
                                        sortedKnownCards[3][0] = "Jack"
                                    elif sortedKnownCards[3][0]== 12:
                                        sortedKnownCards[3][0] = "Queen"
                                    elif sortedKnownCards[3][0]== 13:
                                        sortedKnownCards[3][0] = "King"
                                    else:
                                        pass
                                    
                                    Moves.allPlayers[1].playersCardsDictionary["players"][tempPlayersCardsValue[2]][tempPlayersCardsValue[3]] = (str(playersCardsValue[0][0]),str(playersCardsValue[0][1])) 
                                    if tempPlayersCardsValue[2] == "player1":       #changes AI players dictionary to new card
                                        a = 0
                                    elif tempPlayersCardsValue[2] == "player3":
                                        a = 2
                                    else:
                                        a = 3
                                    Moves.allPlayers[a].cards[playersCardsValue[0][3]-1] = (str(playersCardsValue[0][0]),str(playersCardsValue[0][1]))    #swap the other players card with thier card
                                    Moves.allPlayers[1].cards[sortedKnownCards[3][2]] = (str(sortedKnownCards[3][0]),str(sortedKnownCards[3][1]))    #swap own players card with new one
                                    print(f"player {Moves.allPlayers[i].playerNumber} has swapped their card {sortedKnownCards[3][2]+1} with {playersCardsValue[0][2]}'s card {playersCardsValue[0][3]}")
                            discardPile.append(newCard)
                                
                            time.sleep(5)
                        
                        elif newCard[0] == "Queen":     #miss a go
                            print(f"PLAYER {Moves.allPlayers[i].playerNumber} HAS PLAYED A QUEEN")
                            a = Moves.skip(newCard)
                            skip = a[0]
                            newCard = a[1]
                            time.sleep(5)

                        else:
                            for realValue in range (4):
                                if Moves.allPlayers[1].cards[realValue][0] == "Ace":
                                    tempCards.append((1,realValue))
                                elif Moves.allPlayers[1].cards[realValue][0] == "Jack":
                                    tempCards.append((11,realValue))
                                elif Moves.allPlayers[1].cards[realValue][0] == "Queen":
                                    tempCards.append((12,realValue))
                                elif Moves.allPlayers[1].cards[realValue][0] == "King":
                                    tempCards.append((13,realValue))
                                else:
                                    tempCards.append((int(Moves.allPlayers[1].cards[realValue][0]),realValue))  #the tempCards holds the (cardsValue,cardsPosition) as a list
                            
                            tempCards = merge_sort(tempCards) #sorts the tempCards by their value, lowest to highest
                                      

                            tempNewCard = newCard[0]
                            if newCard[0]== "Ace":
                                tempNewCard = 1
                            elif newCard[0]== "Jack":
                                tempNewCard = 11
                            elif newCard[0]== "Queen":
                                tempNewCard = 12
                            elif newCard[0]== "King":
                                tempNewCard = 13

                            remember = False
                            if percentage == 50:
                                if 1 <= probability and probability <= 5:
                                    remember = True
                            elif percentage == 70:
                                if 1 <= probability and probability <= 7:
                                    remember = True
                            else:
                                if 1 <= probability and probability <= 9:
                                    remember = True
                            if remember == True:
                                if tempCards[3][0] > int(tempNewCard):               #if the last cards value is greater than the new card, swap the cards
                                    Moves.allPlayers[1].cards[tempCards[3][1]] = newCard
                                    newCard = Moves.discard(discardPile ,newCard)
                                    print(f"player {Moves.allPlayers[i].playerNumber} has swapped their card in poisition {tempCards[3][1] + 1} with the new card")
                                else:
                                    discardPile.append(newCard)
                            time.sleep(5)

                        print(f"PLAYER {Moves.allPlayers[i].playerNumber} HAS FINISHED THEIR TURN\n")
                        print("TABLE AT END OF TURN")
                        table = createTable(table,p1.cards,p2.cards,p3.cards,p4.cards) #create the table with actual cards
                        #displayTable(table)
                        virtualTable = createVirtualTable(table,p1.cards,p2.cards,p3.cards,p4.cards)        #create the table with virtual cards
                        displayTable(virtualTable)
                        if len(discardPile) !=0:
                            print(f"discard pile: {discardPile[len(discardPile) -1]}")

                        done = True             #go finished
                        i = 5
                        time.sleep(10)

                    while i == 2:        #player 3 AI

                        difficulty = Moves.allPlayers[i].difficulty
                        probability = random.randint(1,10)
                        forget = random.randint(1,100)
                        percentage = 0
                        if difficulty == 1:
                            percentage = 50
                        elif difficulty == 2:
                            percentage = 70
                        elif difficulty == 3:
                            percentage = 90
                                    
                        if Round == 1:
                            temp = Moves.lookAtCardsStartofRound(p3.cards,0,1)
                            knownCards = [list(temp[0]),list(temp[1])]
                            knownCards.append([None,None])
                            knownCards.append([None,None])
                        tempCards = []
                        Items = ["draw","deck"]
                        drawACardChances = 0

                        cardValue = []
                        for j in p3.cards:
                            if j[0] == "Ace":
                                cardValue.append(1)
                            elif j[0] == "Jack":
                                cardValue.append(11)
                            elif j[0] == "Queen":
                                cardValue.append(12)
                            elif j[0] == "King":
                                cardValue.append(13)
                            else:
                                cardValue.append(int(j[0]))
                        
                        if sum(cardValue) <= 5:
                            print(f"PLAYER {Moves.allPlayers[i].playerNumber} HAS SAID GANDALF!")
                            print("FINAL ROUND")
                            Gandalf = True
                            done = True             #go finished
                            i = 5
                            print("TABLE AT END OF TURN")
                            table = createTable(table,p1.cards,p2.cards,p3.cards,p4.cards) #create the table with actual cards
                            #displayTable(table)
                            virtualTable = createVirtualTable(table,p1.cards,p2.cards,p3.cards,p4.cards)        #create the table with virtual cards
                            displayTable(virtualTable)
                            if len(discardPile) !=0:
                                print(f"discard pile: {discardPile[len(discardPile) -1]}")  

                        newCard = Moves.drawCommand(Items,deck,discardPile,drawACardChances)        #draw card
                        time.sleep(5)

                        if newCard[0] == "7" or newCard[0] == "8":          #play 7 or 8
                            seenCard = Moves.lookAtOwnCard(p3.cards, newCard, i, p3.playerNumber, 2)
                            knownCards.append(seenCard)
                            newCard = (None,None)
                            time.sleep(5)

                        
                        elif newCard[0] == "9" or newCard[0] == "10":       #play 9 or 10
                            print(f"PLAYER {Moves.allPlayers[i].playerNumber} HAS PLAYED A {newCard[0]}")
                            listOfCards = Moves.lookAtSomeoneElsesCard(newCard, Moves.allPlayers[i].difficulty, Moves.allPlayers[i].playerNumber, i)
                            playerNumber = listOfCards[0]
                            position = listOfCards[1]
                            playerCard = listOfCards[2]

                            if playerNumber == 1:
                                playerNumber = "player1"
                            elif playerNumber == 2:
                                playerNumber = "player2"
                            elif playerNumber == 4:
                                playerNumber = "player4"
                            if position == 0:
                                position = "card1"
                            elif position == 1:
                                position = "card2"
                            elif position == 2:
                                position = "card3"
                            else:
                                position = "card4"

                            if percentage == 50:
                                if 1 <= probability and probability <= 5:
                                    if forget <= 10:
                                        Moves.allPlayers[i].playersCardsDictionary["players"][playerNumber][position] = deck.peek(0)
                                    else:
                                        Moves.allPlayers[i].playersCardsDictionary["players"][playerNumber][position] = playerCard
                            elif percentage == 70:
                                if 1 <= probability and probability <= 7:
                                    if forget <= 6:
                                        Moves.allPlayers[i].playersCardsDictionary["players"][playerNumber][position] = deck.peek(0)
                                    else:
                                        Moves.allPlayers[i].playersCardsDictionary["players"][playerNumber][position] = playerCard
                            else:
                                if 1 <= probability and probability <= 9:
                                    if forget == 1:
                                        Moves.allPlayers[i].playersCardsDictionary["players"][playerNumber][position] = deck.peek(0)
                                    else:
                                        Moves.allPlayers[i].playersCardsDictionary["players"][playerNumber][position] = playerCard

                                print(f"player {Moves.allPlayers[i].playerNumber} has seen {playerNumber}'s {position} ")

                            time.sleep(5)

                        elif newCard[0] == "Jack":      #need to learn how to read hashtable/dictionary 
                            playersCardsValue = []
                            for key in Moves.allPlayers[i].playersCardsDictionary["players"].keys():
                                x =1
                                for value in Moves.allPlayers[i].playersCardsDictionary["players"][key].values():
                                    value = [value[0],value[1]]
                                    if value == [None,None]:
                                        pass
                                        x = x+1
                                    else:
                                        if value[0]== "Ace":
                                            value[0]= 1
                                        elif value[0]== "Jack":
                                            value[0] = 11
                                        elif value[0]== "Queen":
                                            value[0] = 12
                                        elif value[0]== "King":
                                            value[0] = 13
                                        else:
                                            value[0]= int(value[0])
                                        playersCardsValue.append([value[0],value[1],key,x])   #card value, card suit, playernumber, card position
                                        x = x+1

                            playersCardsValue = merge_sort(playersCardsValue)

                            sortedKnownCards = []
                            for val in range(len(knownCards)):
                                Rval = 0
                                if knownCards[val][0]== "Ace":
                                    Rval= 1
                                elif knownCards[val][0]== "Jack":
                                    Rval = 11
                                elif knownCards[val][0]== "Queen":
                                    Rval= 12
                                elif knownCards[val][0]== "King":
                                    Rval= 13
                                elif knownCards[val][0]== None:
                                    Rval= 0
                                else:
                                    Rval= int(knownCards[val][0])
                                sortedKnownCards.append([Rval,knownCards[val][1],val]) #card value, card suit, card position
                            sortedKnownCards = merge_sort(sortedKnownCards)

                            playerNumberList = [0,1,3]
                            playerNumber = playerNumberList[random.randint(0,2)]
                            playerNumbersCardPosition = random.randint(0,3)
                            
                            rememebers = False

                            if percentage == 50:
                                if 1 <= probability and probability <= 5:
                                    temporaryCard = p3.cards[0]
                                    p3.cards[0] = Moves.allPlayers[playerNumberList[playerNumber]].cards[playerNumbersCardPosition]
                                    Moves.allPlayers[playerNumberList[playerNumber]].cards[playerNumbersCardPosition] = temporaryCard
                                    print(f"player {Moves.allPlayers[i].playerNumber} swapped cards with player {playerNumber + 1}'s card {playerNumbersCardPosition}")
                                else:
                                    rememebers = True 
                            elif percentage == 70:
                                if 1 <= probability and probability <= 3:
                                    temporaryCard = p3.cards[0]
                                    p3.cards[0] = Moves.allPlayers[playerNumberList[playerNumber]].cards[playerNumbersCardPosition]
                                    Moves.allPlayers[playerNumberList[playerNumber]].cards[playerNumbersCardPosition] = temporaryCard 
                                    print(f"player {Moves.allPlayers[i].playerNumber} swapped cards with player {playerNumber + 1}'s card {playerNumbersCardPosition}")
                                else:
                                    rememebers = True 
                            else:
                                if 1 == probability:
                                    temporaryCard = p3.cards[0]
                                    p3.cards[0] = Moves.allPlayers[playerNumberList[playerNumber]].cards[playerNumbersCardPosition]
                                    Moves.allPlayers[playerNumberList[playerNumber]].cards[playerNumbersCardPosition] = temporaryCard 
                                    print(f"player {Moves.allPlayers[i].playerNumber} swapped cards with player {playerNumber + 1}'s card {playerNumbersCardPosition}")
                                else:
                                    rememebers = True 

                            if rememebers == True:

                                if len(playersCardsValue) == 0:
                                    pass
                                elif sortedKnownCards[3][0] > playersCardsValue[0][0]:      #swaps AI players highest card with the known lowest card
                                    tempKnownCard = list(sortedKnownCards[3])
                                    tempPlayersCardsValue = list(playersCardsValue[0])

                                    sortedKnownCards[3][0] = tempPlayersCardsValue[0]
                                    sortedKnownCards[3][1] = tempPlayersCardsValue[1]

                                    playersCardsValue[0][0]= tempKnownCard[0]
                                    playersCardsValue[0][1]= tempKnownCard[1]
                                    print(playersCardsValue)
                                    if playersCardsValue[0][0]== 1:
                                        playersCardsValue[0][0] = "Ace"
                                    elif playersCardsValue[0][0]== 11:
                                        playersCardsValue[0][0] = "Jack"
                                    elif playersCardsValue[0][0]== 12:
                                        playersCardsValue[0][0] = "Queen"
                                    elif playersCardsValue[0][0]== 13:
                                        playersCardsValue[0][0] = "King"
                                    else:
                                        pass
                                    if sortedKnownCards[3][0]== 1:
                                        sortedKnownCards[3][0] = "Ace"
                                    elif psortedKnownCards[3][0]== 11:
                                        sortedKnownCards[3][0] = "Jack"
                                    elif sortedKnownCards[3][0]== 12:
                                        sortedKnownCards[3][0] = "Queen"
                                    elif sortedKnownCards[3][0]== 13:
                                        sortedKnownCards[3][0] = "King"
                                    else:
                                        pass
                                    
                                    Moves.allPlayers[i].playersCardsDictionary["players"][tempPlayersCardsValue[2]][tempPlayersCardsValue[3]] = (str(playersCardsValue[0][0]),str(playersCardsValue[0][1])) #chnages AI players dictionary to new card
                                    if tempPlayersCardsValue[2] == "player1":
                                        a = 0
                                    elif tempPlayersCardsValue[2] == "player2":
                                        a = 1
                                    else:
                                        a = 3
                                    Moves.allPlayers[a].cards[playersCardsValue[0][3]-1] = (str(playersCardsValue[0][0]),str(playersCardsValue[0][1]))    #swap the other players card with thier card
                                    Moves.allPlayers[i].cards[sortedKnownCards[3][2]] = (str(sortedKnownCards[3][0]),str(sortedKnownCards[3][1]))    #swap own players card with new one
                                    print(f"player {Moves.allPlayers[i].playerNumber} has swapped their card {sortedKnownCards[3][2]+1} with {playersCardsValue[0][2]}'s card {playersCardsValue[0][3]}")
                            discardPile.append(newCard)
                                
                            time.sleep(5)
                        
                        elif newCard[0] == "Queen":     #miss a go
                            print(f"PLAYER {Moves.allPlayers[i].playerNumber} HAS PLAYED A QUEEN")
                            a = Moves.skip(newCard)
                            skip = a[0]
                            newCard = a[1]
                            time.sleep(5)

                        else:
                            for realValue in range (4):
                                if Moves.allPlayers[i].cards[realValue][0] == "Ace":
                                    tempCards.append((1,realValue))
                                elif Moves.allPlayers[i].cards[realValue][0] == "Jack":
                                    tempCards.append((11,realValue))
                                elif Moves.allPlayers[i].cards[realValue][0] == "Queen":
                                    tempCards.append((12,realValue))
                                elif Moves.allPlayers[i].cards[realValue][0] == "King":
                                    tempCards.append((13,realValue))
                                else:
                                    tempCards.append((int(Moves.allPlayers[i].cards[realValue][0]),realValue))  #the tempCards holds the (cardsValue,cardsPosition) as a list
                            
                            tempCards = merge_sort(tempCards) #sorts the tempCards by their value, lowest to highest
                                      

                            tempNewCard = newCard[0]
                            if newCard[0]== "Ace":
                                tempNewCard = 1
                            elif newCard[0]== "Jack":
                                tempNewCard = 11
                            elif newCard[0]== "Queen":
                                tempNewCard = 12
                            elif newCard[0]== "King":
                                tempNewCard = 13

                            remember = False
                            if percentage == 50:
                                if 1 <= probability and probability <= 5:
                                    remember = True
                            elif percentage == 70:
                                if 1 <= probability and probability <= 7:
                                    remember = True
                            else:
                                if 1 <= probability and probability <= 9:
                                    remember = True
                            if remember == True:
                                if tempCards[3][0] > int(tempNewCard):               #if the last cards value is greater than the new card, swap the cards
                                    Moves.allPlayers[i].cards[tempCards[3][1]] = newCard
                                    newCard = Moves.discard(discardPile ,newCard)
                                    print(f"player {Moves.allPlayers[i].playerNumber} has swapped their card in poisition {tempCards[3][1] + 1} with the new card")
                                else:
                                    discardPile.append(newCard)
        
                            time.sleep(5)

                        print(f"PLAYER {Moves.allPlayers[i].playerNumber} HAS FINISHED THEIR TURN\n")
                        print("TABLE AT END OF TURN")
                        table = createTable(table,p1.cards,p2.cards,p3.cards,p4.cards) #create the table with actual cards
                        #displayTable(table)
                        virtualTable = createVirtualTable(table,p1.cards,p2.cards,p3.cards,p4.cards)        #create the table with virtual cards
                        displayTable(virtualTable)
                        if len(discardPile) !=0:
                            print(f"discard pile: {discardPile[len(discardPile) -1]}")

                        done = True             #go finished
                        i = 5
                        time.sleep(10)
                        
                    while i == 3:               #player 4 AI
                        difficulty = Moves.allPlayers[i].difficulty
                        probability = random.randint(1,10)
                        forget = random.randint(1,100)
                        percentage = 0
                        if difficulty == 1:
                            percentage = 50
                        elif difficulty == 2:
                            percentage = 70
                        elif difficulty == 3:
                            percentage = 90
                                    
                        if Round == 1:
                            temp = Moves.lookAtCardsStartofRound(p4.cards,0,1)
                            knownCards = [list(temp[0]),list(temp[1])]
                            knownCards.append([None,None])
                            knownCards.append([None,None])
                        tempCards = []
                        Items = ["draw","deck"]
                        drawACardChances = 0

                        cardValue = []
                        for j in p4.cards:
                            if j[0] == "Ace":
                                cardValue.append(1)
                            elif j[0] == "Jack":
                                cardValue.append(11)
                            elif j[0] == "Queen":
                                cardValue.append(12)
                            elif j[0] == "King":
                                cardValue.append(13)
                            else:
                                cardValue.append(int(j[0]))
                        
                        if sum(cardValue) <= 5:
                            print(f"PLAYER {Moves.allPlayers[i].playerNumber} HAS SAID GANDALF!")
                            print("FINAL ROUND")
                            Gandalf = True
                            done = True             #go finished
                            i = 5
                            print("TABLE AT END OF TURN")
                            table = createTable(table,p1.cards,p2.cards,p3.cards,p4.cards) #create the table with actual cards
                            #displayTable(table)
                            virtualTable = createVirtualTable(table,p1.cards,p2.cards,p3.cards,p4.cards)        #create the table with virtual cards
                            displayTable(virtualTable)
                            if len(discardPile) !=0:
                                print(f"discard pile: {discardPile[len(discardPile) -1]}")  

                        newCard = Moves.drawCommand(Items,deck,discardPile,drawACardChances)        #draw card
                        time.sleep(5)

                        if newCard[0] == "7" or newCard[0] == "8":          #play 7 or 8
                            seenCard = Moves.lookAtOwnCard(p4.cards, newCard, i, p4.playerNumber, 2)
                            knownCards.append(seenCard)
                            newCard = (None,None)
                            time.sleep(5)

                        
                        elif newCard[0] == "9" or newCard[0] == "10":       #play 9 or 10
                            print(f"PLAYER {Moves.allPlayers[i].playerNumber} HAS PLAYED A {newCard[0]}")
                            listOfCards = Moves.lookAtSomeoneElsesCard(newCard, Moves.allPlayers[i].difficulty, Moves.allPlayers[i].playerNumber, i)
                            playerNumber = listOfCards[0]
                            position = listOfCards[1]
                            playerCard = listOfCards[2]

                            if playerNumber == 1:
                                playerNumber = "player1"
                            elif playerNumber == 2:
                                playerNumber = "player2"
                            elif playerNumber == 3:
                                playerNumber = "player3"
                            if position == 0:
                                position = "card1"
                            elif position == 1:
                                position = "card2"
                            elif position == 2:
                                position = "card3"
                            else:
                                position = "card4"

                            if percentage == 50:
                                if 1 <= probability and probability <= 5:
                                    if forget <= 10:
                                        Moves.allPlayers[i].playersCardsDictionary["players"][playerNumber][position] = deck.peek(0)
                                    else:
                                        Moves.allPlayers[i].playersCardsDictionary["players"][playerNumber][position] = playerCard
                            elif percentage == 70:
                                if 1 <= probability and probability <= 7:
                                    if forget <= 6:
                                        Moves.allPlayers[i].playersCardsDictionary["players"][playerNumber][position] = deck.peek(0)
                                    else:
                                        Moves.allPlayers[i].playersCardsDictionary["players"][playerNumber][position] = playerCard
                            else:
                                if 1 <= probability and probability <= 9:
                                    if forget == 1:
                                        Moves.allPlayers[i].playersCardsDictionary["players"][playerNumber][position] = deck.peek(0)
                                    else:
                                        Moves.allPlayers[i].playersCardsDictionary["players"][playerNumber][position] = playerCard

                                print(f"player {Moves.allPlayers[i].playerNumber} has seen {playerNumber}'s {position} ")

                            time.sleep(5)

                        elif newCard[0] == "Jack":       
                            playersCardsValue = []
                            for key in Moves.allPlayers[i].playersCardsDictionary["players"].keys():
                                x =1
                                for value in Moves.allPlayers[i].playersCardsDictionary["players"][key].values():
                                    value = [value[0],value[1]]
                                    if value == [None,None]:
                                        pass
                                        x = x+1
                                    else:
                                        if value[0]== "Ace":
                                            value[0]= 1
                                        elif value[0]== "Jack":
                                            value[0] = 11
                                        elif value[0]== "Queen":
                                            value[0] = 12
                                        elif value[0]== "King":
                                            value[0] = 13
                                        else:
                                            value[0]= int(value[0])
                                        playersCardsValue.append([value[0],value[1],key,x])   #card value, card suit, playernumber, card position
                                        x = x+1

                            playersCardsValue = merge_sort(playersCardsValue)
                            print(playersCardsValue)

                            sortedKnownCards = []
                            for val in range(len(knownCards)):
                                Rval = 0
                                if knownCards[val][0]== "Ace":
                                    Rval= 1
                                elif knownCards[val][0]== "Jack":
                                    Rval = 11
                                elif knownCards[val][0]== "Queen":
                                    Rval= 12
                                elif knownCards[val][0]== "King":
                                    Rval= 13
                                elif knownCards[val][0]== None:
                                    Rval= 0
                                else:
                                    Rval= int(knownCards[val][0])
                                sortedKnownCards.append([Rval,knownCards[val][1],val]) #card value, card suit, card position
                            sortedKnownCards = merge_sort(sortedKnownCards)

                            playerNumberList = [0,1,2]
                            playerNumber = playerNumberList[random.randint(0,2)]
                            playerNumbersCardPosition = random.randint(0,3)
                            
                            rememebers = False

                            if percentage == 50:
                                if 1 <= probability and probability <= 5:
                                    temporaryCard = p4.cards[0]
                                    p4.cards[0] = Moves.allPlayers[playerNumberList[playerNumber]].cards[playerNumbersCardPosition]
                                    Moves.allPlayers[playerNumberList[playerNumber]].cards[playerNumbersCardPosition] = temporaryCard
                                    print(f"player {Moves.allPlayers[i].playerNumber} swapped cards with player {playerNumber + 1}'s card {playerNumbersCardPosition}")
                                else:
                                    rememebers = True 
                            elif percentage == 70:
                                if 1 <= probability and probability <= 3:
                                    temporaryCard = p4.cards[0]
                                    p4.cards[0] = Moves.allPlayers[playerNumberList[playerNumber]].cards[playerNumbersCardPosition]
                                    Moves.allPlayers[playerNumberList[playerNumber]].cards[playerNumbersCardPosition] = temporaryCard 
                                    print(f"player {Moves.allPlayers[i].playerNumber} swapped cards with player {playerNumber + 1}'s card {playerNumbersCardPosition}")
                                else:
                                    rememebers = True 
                            else:
                                if 1 == probability:
                                    temporaryCard = p4.cards[0]
                                    p4.cards[0] = Moves.allPlayers[playerNumberList[playerNumber]].cards[playerNumbersCardPosition]
                                    Moves.allPlayers[playerNumberList[playerNumber]].cards[playerNumbersCardPosition] = temporaryCard 
                                    print(f"player {Moves.allPlayers[i].playerNumber} swapped cards with player {playerNumber + 1}'s card {playerNumbersCardPosition}")
                                else:
                                    rememebers = True 

                            if rememebers == True:

                                if len(playersCardsValue) == 0:
                                    pass
                                elif sortedKnownCards[3][0] > playersCardsValue[0][0]:      #swaps AI players highest card with the known lowest card
                                    tempKnownCard = list(sortedKnownCards[3])
                                    tempPlayersCardsValue = list(playersCardsValue[0])

                                    sortedKnownCards[3][0] = tempPlayersCardsValue[0]
                                    sortedKnownCards[3][1] = tempPlayersCardsValue[1]

                                    playersCardsValue[0][0]= tempKnownCard[0]
                                    playersCardsValue[0][1]= tempKnownCard[1]
                                    if playersCardsValue[0][0]== 1:
                                        playersCardsValue[0][0] = "Ace"
                                    elif playersCardsValue[0][0]== 11:
                                        playersCardsValue[0][0] = "Jack"
                                    elif playersCardsValue[0][0]== 12:
                                        playersCardsValue[0][0] = "Queen"
                                    elif playersCardsValue[0][0]== 13:
                                        playersCardsValue[0][0] = "King"
                                    else:
                                        pass
                                    if sortedKnownCards[3][0]== 1:
                                        sortedKnownCards[3][0] = "Ace"
                                    elif psortedKnownCards[3][0]== 11:
                                        sortedKnownCards[3][0] = "Jack"
                                    elif sortedKnownCards[3][0]== 12:
                                        sortedKnownCards[3][0] = "Queen"
                                    elif sortedKnownCards[3][0]== 13:
                                        sortedKnownCards[3][0] = "King"
                                    else:
                                        pass

                                    Moves.allPlayers[i].playersCardsDictionary["players"][tempPlayersCardsValue[2]][tempPlayersCardsValue[3]] = (str(playersCardsValue[0][0]),str(playersCardsValue[0][1])) #chnages AI players dictionary to new card
                                    if tempPlayersCardsValue[2] == "player1":
                                        a = 0
                                    elif tempPlayersCardsValue[2] == "player2":
                                        a = 1
                                    else:
                                        a = 2
                                    Moves.allPlayers[a].cards[playersCardsValue[0][3]-1] = (str(playersCardsValue[0][0]),str(playersCardsValue[0][1]))    #swap the other players card with thier card
                                    Moves.allPlayers[i].cards[sortedKnownCards[3][2]] = (str(sortedKnownCards[3][0]),str(sortedKnownCards[3][1]))    #swap own players card with new one
                                    print(f"player {Moves.allPlayers[i].playerNumber} has swapped their card {sortedKnownCards[3][2]+1} with {playersCardsValue[0][2]}'s card {playersCardsValue[0][3]}")
                            discardPile.append(newCard)
                                
                            time.sleep(5)
                        
                        elif newCard[0] == "Queen":     #miss a go
                            print(f"PLAYER {Moves.allPlayers[i].playerNumber} HAS PLAYED A QUEEN")
                            a = Moves.skip(newCard)
                            skip = a[0]
                            newCard = a[1]
                            time.sleep(5)

                        else:
                            for realValue in range (4):
                                if Moves.allPlayers[i].cards[realValue][0] == "Ace":
                                    tempCards.append((1,realValue))
                                elif Moves.allPlayers[i].cards[realValue][0] == "Jack":
                                    tempCards.append((11,realValue))
                                elif Moves.allPlayers[i].cards[realValue][0] == "Queen":
                                    tempCards.append((12,realValue))
                                elif Moves.allPlayers[i].cards[realValue][0] == "King":
                                    tempCards.append((13,realValue))
                                else:
                                    tempCards.append((int(Moves.allPlayers[i].cards[realValue][0]),realValue))  #the tempCards holds the (cardsValue,cardsPosition) as a list
                            
                            tempCards = merge_sort(tempCards) #sorts the tempCards by their value, lowest to highest
                                      

                            tempNewCard = newCard[0]
                            if newCard[0]== "Ace":
                                tempNewCard = 1
                            elif newCard[0]== "Jack":
                                tempNewCard = 11
                            elif newCard[0]== "Queen":
                                tempNewCard = 12
                            elif newCard[0]== "King":
                                tempNewCard = 13

                            remember = False
                            if percentage == 50:
                                if 1 <= probability and probability <= 5:
                                    remember = True
                            elif percentage == 70:
                                if 1 <= probability and probability <= 7:
                                    remember = True
                            else:
                                if 1 <= probability and probability <= 9:
                                    remember = True
                            if remember == True:
                                if tempCards[3][0] > int(tempNewCard):               #if the last cards value is greater than the new card, swap the cards
                                    Moves.allPlayers[i].cards[tempCards[3][1]] = newCard
                                    newCard = Moves.discard(discardPile ,newCard)
                                    print(f"player {Moves.allPlayers[i].playerNumber} has swapped their card in poisition {tempCards[3][1] + 1} with the new card")
                                else:  
                                    discardPile.append(newCard)
                            time.sleep(5)

                        print(f"PLAYER {Moves.allPlayers[i].playerNumber} HAS FINISHED THEIR TURN\n")
                        print("TABLE AT END OF TURN")
                        table = createTable(table,p1.cards,p2.cards,p3.cards,p4.cards) #create the table with actual cards
                        #displayTable(table)
                        virtualTable = createVirtualTable(table,p1.cards,p2.cards,p3.cards,p4.cards)        #create the table with virtual cards
                        displayTable(virtualTable)
                        if len(discardPile) !=0:
                            print(f"discard pile: {discardPile[len(discardPile) -1]}")

                        done = True             #go finished
                        i = 5
                        time.sleep(10)
                    
            else:
                print(f"***PLAYER {Moves.allPlayers[i].playerNumber} MISSES A GO***")
                skip = False    #if queen is used to skip then when its the next players turn it will skip the whole code and go to the next players turn
                done = True
            
    print("END OF GAME")

    orderList = []

    for i in range (4):
        x = int(len(Moves.allPlayers[i].cards)) 
        for j in range (x):
            if Moves.allPlayers[i].cards[j][0] == "Ace":
                Moves.allPlayers[i].totalPoints =  Moves.allPlayers[i].totalPoints + 1
            elif Moves.allPlayers[i].cards[j][0] == "Jack":
                Moves.allPlayers[i].totalPoints =  Moves.allPlayers[i].totalPoints + 11
            elif Moves.allPlayers[i].cards[j][0] == "Queen":
                Moves.allPlayers[i].totalPoints =  Moves.allPlayers[i].totalPoints + 12
            elif Moves.allPlayers[i].cards[j][0] == "King":
                Moves.allPlayers[i].totalPoints =  Moves.allPlayers[i].totalPoints + 13
            else:
                Moves.allPlayers[i].totalPoints = Moves.allPlayers[i].totalPoints + int(Moves.allPlayers[i].cards[j][0])
        orderList.append([Moves.allPlayers[i].totalPoints + Moves.allPlayers[i].mistakeCounter, i+1])


    orderList = merge_sort(orderList)
   

    print("\n")
    print("*****FINAL TABLE *****")
    print("\n")
    print( "POSITION| PLAYER NUMBER  |  VALUE OF CARDS | PENALTY POINTS | OVERALL SCORE |")
    print(f"FIRST   |       {orderList[0][1]}        |        {orderList[0][0] - Moves.allPlayers[0].mistakeCounter}       |        {Moves.allPlayers[0].mistakeCounter}       |       {orderList[0][0]}      |")
    print(f"SECOND  |       {orderList[1][1]}        |        {orderList[1][0] - Moves.allPlayers[0].mistakeCounter}       |        {Moves.allPlayers[0].mistakeCounter}       |       {orderList[1][0]}      |")
    print(f"THIRD   |       {orderList[2][1]}        |        {orderList[2][0] - Moves.allPlayers[0].mistakeCounter}       |        {Moves.allPlayers[0].mistakeCounter}       |       {orderList[2][0]}      |")
    print(f"FORUTH  |       {orderList[3][1]}        |        {orderList[3][0] - Moves.allPlayers[0].mistakeCounter}       |        {Moves.allPlayers[0].mistakeCounter}       |       {orderList[3][0]}      |")
    
    



loadGame = input("do you want to load a previous games?")
if loadGame == "yes":
    gameFile = input("what is the file name of the game you want to load: ")
    print(f"loading {gameFile}...")
    with open(f'{gameFile}.txt') as f:
        tempDeck = eval(f.readline())
        discardPile = eval(f.readline())
        c1 = eval(f.readline())
        c2 = eval(f.readline())
        c3 = eval(f.readline())
        c4 = eval(f.readline())
        p1m = int(f.readline())
        p2m = int(f.readline())
        p3m = int(f.readline())
        p4m = int(f.readline())
        p2d = int(f.readline())
        p3d = int(f.readline())
        p4d = int(f.readline())
        temp2 = f.readline()
        P2playersCards = eval(temp2)
        temp3 = f.readline()
        P3playersCards = eval(temp3)
        temp4 = f.readline()
        P4playersCards = eval(temp4)

    deck = Stack()
    for i in range (len(tempDeck)):
        deck.push(tempDeck[i])

    
    p1 = Player(1,c1,0,p1m,0)
    p2 = AIPlayer(2,c2,0,p2m,p2d,P2playersCards)
    p3 = AIPlayer(3,c3,0,p3m,p3d,P3playersCards)
    p4 = AIPlayer(4,c4,0,p4m,p4d,P4playersCards)

    rows, cols = (6,6) 
    table = [[" " for i in range(cols)] for j in range(rows)]               #table stores the acctual cards and vitural table is what the players see (the back of the card - x)
    virtualTable = [[" " for i in range(cols)] for j in range(rows)] 

    table = createTable(table,p1.cards,p2.cards,p3.cards,p4.cards)
    virtualTable = createVirtualTable(table,p1.cards,p2.cards,p3.cards,p4.cards)

    Moves = Moves(deck,p1,p2,p3,p4,discardPile)
    main(Moves,discardPile,Card,Stack,Player,table,virtualTable,True)

else:
    
    if __name__ == "__main__":
        rows, cols = (6,6) 
        table = [[" " for i in range(cols)] for j in range(rows)]               #table stores the acctual cards and vitural table is what the players see (the back of the card - x)
        virtualTable = [[" " for i in range(cols)] for j in range(rows)] 

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

        c1 = []
        c2 = []
        c3 = []
        c4 = []
        for i in range (0,4):
            c1.append(deck.pop())
            c2.append(deck.pop())
            c3.append(deck.pop())
            c4.append(deck.pop())
        


        discardPile = []

        P2playersCards = {"players": {"player1":{"card1":(None,None), "card2":(None,None), "card3":(None,None), "card4":(None,None)},       #hash dictionaries to store known players cards
                                    "player3":{"card1":(None,None), "card2":(None,None), "card3":(None,None), "card4":(None,None)},
                                    "player4":{"card1":(None,None), "card2":(None,None), "card3":(None,None), "card4":(None,None)}}}

        P3playersCards = {"players": {"player1":{"card1":(None,None), "card2":(None,None), "card3":(None,None), "card4":(None,None)},
                                    "player2":{"card1":(None,None), "card2":(None,None), "card3":(None,None), "card4":(None,None)},
                                    "player4":{"card1":(None,None), "card2":(None,None), "card3":(None,None), "card4":(None,None)}}}

        P4playersCards = {"players": {"player1":{"card1":(None,None), "card2":(None,None), "card3":(None,None), "card4":(None,None)},
                                    "player2":{"card1":(None,None), "card2":(None,None), "card3":(None,None), "card4":(None,None)},
                                    "player3":{"card1":(None,None), "card2":(None,None), "card3":(None,None), "card4":(None,None)}}}

        p1 = Player(1,c1,0,0,0)
        p2 = AIPlayer(2,c2,0,0,0,P2playersCards)
        p3 = AIPlayer(3,c3,0,0,0,P3playersCards)
        p4 = AIPlayer(4,c4,0,0,0,P4playersCards)

        Moves = Moves(deck,p1,p2,p3,p4,discardPile)            #this passes in the parameters neccesary for class move 
        main(Moves,discardPile,Card,Stack,Player,table,virtualTable,False)


