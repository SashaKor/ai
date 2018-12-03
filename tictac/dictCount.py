''' Layout positions:
0 1 2
3 4 5
6 7 8
'''
# layouts look like "_x_ox__o_"

Wins = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]

AllBoards = {} # this is a dictionary with key = a layout, and value = its corresponding BoardNode
turn= "x" #initial turn

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

def CreateAllBoards(layout,parent):
    # recursive function to manufacture all BoardNode nodes and place them into the AllBoards dictionary
    global AllBoards,turn
    if not(layout in AllBoards):
        AllBoards[layout]= BoardNode(layout)
    AllBoards[layout].parents.append(parent)

    if won(layout,'x'):
        AllBoards[layout].endState = 'x'
    if won(layout,"o"):
        AllBoards[layout].endState = 'o'
    if draw(layout):
        AllBoards[layout].endState = 'd'
    else:
        for i in range(0,9):
            if layout[i]== "_":
                 child= layout[:i]+turn+layout[i+1:]
                 AllBoards[layout].children.append(child)
                 if turn == "x":
                     turn= "o"
                 CreateAllBoards(child,layout)
                 layout= layout[:i]+"_"+layout[i+1:]
posGames=0
posBoards=[]

def buildTree():
    start="_________"
    return helpBuildTree(start,"x")

#passing in board and who currently moving
def helpBuildTree(board,turn):
    global posGames,posBoards
    if won(board,'x') or won(board,"o") or draw(board):
        posGames+=1
    else:
        for i in range(0,9):
            if board[i]== "_":
                 board= board[:i]+turn+board[i+1:]
                 if not(board in posBoards):
                     posBoards.append(board)
                 helpBuildTree(board,'x' if turn == 'o' else 'o')
                 board= board[:i]+"_"+board[i+1:]

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

CreateAllBoards('_________',None)
print(AllBoards.keys())
