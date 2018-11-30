
'''
Aleksandra Koroza
11/29/18

First homework assignment: count the number of different boards and the number of different possible games (much larger number),
remembering that, by our convention, "x" always moves first.  Write in Comments-to-Teacher: number of boards and number of different games.
Board layout positions, cell numbering:

0 | 1 | 2
---------
3 | 4 | 5
---------
6 | 7 | 8

Board coding: "x" and "o" will be used for moves. "_" (underscore) will be used for unoccupied cells.
'''

posGames=0
posBoards=[]

def buildTree():
    start="_________"
    return helpBuildTree(start,"x",[])

#passing in board and who currently moving
def helpBuildTree(board,turn,lst):
    global posGames,posBoards
    if won(board,'x') or won(board,"o") or draw(board):
        posGames+=1
    else:
        for i in range(0,9):
            if board[i]== "_":
                 board= board[:i]+turn+board[i+1:]
                 if not(board in posBoards):
                     posBoards.append(board)
                 helpBuildTree(board,'x' if turn == 'o' else 'o',lst)
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


buildTree()
print("There are "+str(posGames)+" possible games and "+str(len(posBoards))+" possible boards.")
