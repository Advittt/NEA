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

rows, cols = (6,6) 
table = [[" " for i in range(cols)] for j in range(rows)]               #table stores the acctual cards and vitural table is what the players see (the back of the card - x)
virtualTable = [[" " for i in range(cols)] for j in range(rows)] 

p1 = [randomCard(),randomCard(),randomCard(),randomCard()]
p2 = [randomCard(),randomCard(),randomCard(),randomCard()]              #selects radnom card
p3 = [randomCard(),randomCard(),randomCard(),randomCard()]
p4 = [randomCard(),randomCard(),randomCard(),randomCard()]

    
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

table = createTable(table,p1,p2,p3,p4)
for row in table: 
    for elem in row:
        print(elem, end=' ')        # this is how you display 2d arrays
    print()

for row in createVirtualTable(table,p1,p2,p3,p4):
    for elem in row:
        print(elem, end=' ')
    print()