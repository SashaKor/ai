''' Layout positions:
0 1 2
3 4 5
6 7 8
'''
# layouts look like "_x_ox__o_"

AllBoards = {} # this is a dictionary with key = a layout, and value = its corresponding BoardNode

class BoardNode:
    def __init__(self,layout):
        self.layout = layout
        self.endState = None # if this is a terminal board, endState == 'x' or 'o' for wins, of 'd' for draw, else None
        self.parents = [] # all layouts that can lead to this one, by one move
        self.children = [] # all layouts that can be reached with a single move

    def print_me(self):
        print ('layout:',self.layout, 'endState:',self.endState)
        print ('parents:',self.parents)
        print ('children:',self.children)

# ~encapsulation~
def CreateAllBoards(layout,parent):
    CreateAllBoardsH(layout,parent,"x")

def CreateAllBoardsH(layout,parent,turn):
    # recursive function to manufacture all BoardNode nodes and place them into the AllBoards dictionary
    global AllBoards
    if not(layout in AllBoards):
        AllBoards[layout]= BoardNode(layout)
    AllBoards[layout].parents.append(parent)

    if won(layout,'x'):
        AllBoards[layout].endState = 'x'
    elif won(layout,"o"):
        AllBoards[layout].endState = 'o'
    elif draw(layout):
        AllBoards[layout].endState = 'd'
    else:
        for i in range(0,9):
            if layout[i]== "_":
                 child = layout[:i]+turn+layout[i+1:]
                 AllBoards[layout].children.append(layout)
                 CreateAllBoardsH(child,layout,'x' if turn == 'o' else 'o')
                 child= child[:i]+"_"+ child[i+1:]

#returns True if a certain player won a game
def won(board, player):
    cliques= [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]
    for elem in cliques:
        result=""
        for num in elem:
            result+= board[num]
        if (result == 3*player):
            return True
    return False

#returns True if all spaces filled
def draw(board):
    return (not("_" in board))

#testing
CreateAllBoards('_________',None)
print("Number of boards: " + str(len(AllBoards)))

#4. As a further check, add up the number of children for all of the BoardNodes inside
#AllBoards (yes, that's a huge number of duplications, but it's a check that you've done it right).
# Place that number into the Comments-to-Teacher, and also submit your code file.
numChildren=0
for key in AllBoards.keys():
    numChildren+= len(AllBoards[key].children)
print("Number of children: " + str(numChildren))
# 5. Additionally, calculate and report to the Comments-to-Teacher: the number of boards
# in AllBoards that end in x-winning, o-winning, draws, and the number of boards that are not ends-of-games.
# Also submit any comments on the homework itself, as usual.
numX=0
numO=0
numD=0
numN=0

for key in AllBoards.keys():
    if AllBoards[key].endState== 'x':
        numX += 1
    elif AllBoards[key].endState== 'o':
        numO += 1
    elif AllBoards[key].endState== 'd':
        numD += 1
    else:
        numN += 1

print("Number of x wins: " + str(numX))
print("Number of y wins: " + str(numO))
print("Number of draws: " + str(numD))
print("Number of not end-of-games: " + str(numN))
#print(str(numX+numO+numD+numN))
