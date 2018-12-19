#! /usr/bin/python3
# My ticTacToe competitior


import random, sys

''' Layout positions:
0 1 2
3 4 5
6 7 8
'''
# Best future states according to the player viewing this board
ST_X = 1  # X wins
ST_O = 2  # O wins
ST_D = 3  # Draw

Wins = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]

AllBoards = {}  # This is primarily for debugging: key = layout, value = BoardNode


class BoardNode:
    def __init__(self, layout):
        self.layout = layout
        self.mover = 'x' if layout.count('x') == layout.count('o') else 'o'
        # self.mover = 'o' if layout.count('x') == layout.count('o') else 'x'

        self.state = this_state(layout)  # if final board, then ST_X, ST_O or ST_D, else None
        if self.state is None:
            self.best_final_state = None  # best achievable future state: ST_X, ST_O or ST_D
            self.best_move = None  # 0-9 to achieve best state
            self.num_moves_to_final_state = None  # number of moves to best state
        else:
            self.best_final_state = self.state
            self.best_move = -1
            self.num_moves_to_final_state = 0  # already at final state

        self.children = set()

    def __str__(self):
        return str(self.layout[0:3]) + "|" + str(self.layout[3:6]) + "|" + str(self.layout[6:9])

    def print_me(self):
        print('layout:', self.layout)
        print('mover:', self.mover)
        # print('state:',BoardNode.str_state(self.state))
        print('best_final_state:', BoardNode.str_state(self.best_final_state))
        # print('best_move:',self.best_move,BoardNode.str_move(self.best_move))
        print('num_moves_to_final_state:', self.num_moves_to_final_state)

    def print_layout(self):
        print('%s\n%s\n%s' % (' '.join(self.layout[0:3]), ' '.join(self.layout[3:6]), ' '.join(self.layout[6:9])))

    # =================== class methods  =======================
def str_state(state):
    # human description of a state
    return 'None' if state is None else ['x-wins', 'o-wins', 'draw'][state - 1]

def str_move(move):
# human description of a move
    moves = ('top-left', 'top-center', 'top-right', 'middle-left', 'middle-center', 'middle-right', 'bottom-left',
            'bottom-center', 'bottom-right')
    return 'done' if move == -1 else moves[move]

def this_state(layout):
    # classifies this layout as None if not final, otherwise ST_X or ST_O or ST_D
    for awin in Wins:
        if layout[awin[0]] != '_' and layout[awin[0]] == layout[awin[1]] == layout[awin[2]]:
            return ST_X if layout[awin[0]] == 'x' else ST_O
    if layout.count('_') == 0:
        return ST_D
    return None


def CreateAllBoards(layout):
    # Populate AllBoards with finally calculated BoardNodes
    # print("CreateAllBoards["+layout+"]")

    if layout in AllBoards:
        return

    anode = BoardNode(layout)
    AllBoards[layout] = anode

    # if this is an end board, then all of its properties have already be calculated by __init__()
    if anode.state is not None:
        return

    # expand children if this is not a final state
    for pos in range(9):
        if layout[pos] == '_':
            new_layout = layout[:pos] + anode.mover + layout[pos + 1:]
            if new_layout not in AllBoards:
                CreateAllBoards(new_layout)
            anode.children.add(AllBoards[new_layout])

    for child in anode.children:
        if isChildStateBetter(anode, child):
            anode.best_final_state = child.best_final_state
            anode.best_move = findDiff(anode.layout, child.layout)
            if child.num_moves_to_final_state is not None:
                anode.num_moves_to_final_state = child.num_moves_to_final_state + 1


def findDiff(layout, child_layout):
    for i in range(0, 9):
        if layout[i] != child_layout[i]:
            return i
    return -1


def isChildStateBetter(node, child):
    if node.best_final_state is None:
        return True

    if node.mover == 'x' and child.best_final_state == ST_X:
        if node.best_final_state == ST_X:
            return child.num_moves_to_final_state < node.num_moves_to_final_state
        else:
            return True
    elif node.mover == 'o' and child.best_final_state == ST_O:
        if node.best_final_state == ST_O:
            return child.num_moves_to_final_state < node.num_moves_to_final_state
        else:
            return True
    elif node.mover == 'x' and child.best_final_state == ST_D:
        if node.best_final_state != ST_X:
            if node.best_final_state == ST_D:
                return child.num_moves_to_final_state > node.num_moves_to_final_state
            else:
                return True
    elif node.mover == 'o' and child.best_final_state == ST_D:
        if node.best_final_state != ST_O:
            if node.best_final_state == ST_D:
                return child.num_moves_to_final_state > node.num_moves_to_final_state
            else:
                return True

    return False

Usage = '''
TTT-Random.py board={9-char} result_prefix={prefix} result_file={filename}
       will write a move to filename (if result_file is provided)
       else print move
   or
TTT-Random.py id=1 result_prefix=(prefix) result_file={filename}
       will write AUTHOR and TITLE to filename (if result_file is provided)
       else print them
'''

AUTHOR = 'A. Koroza'
TITLE = 'Not-So Random Mover'

#necessary code massaging
def main():
    if len(sys.argv) < 2:
        print (Usage)
        return
    dct = getargs()
    result = ''
    if 'id' in dct:
        result='author=%s\ntitle=%s\n' % (AUTHOR,TITLE)
    elif 'board' in dct:
        board=dct['board']
        if len(board) != 9:
            result='Error: board must be 9 characters'
        else:
            poss=[i for i in range(9) if board[i]=='_']
            '''
            if len(poss) > 0:
                i = random.choice(poss)
                result='move=%d\n(pretty random, though)\n' % i
            else:
                result='move=-1\n(Come on, the game is done!)\n'
                '''
            if len(poss) > 0:
                CreateAllBoards(board)
                node = AllBoards[board]
                best_move= node.best_move
                result='move=%d\n %s in %d moves!\n' % (best_move,str_state(node.best_final_state),node.num_moves_to_final_state)
            else:
                result='move=-1\n(Come on, the game is done!)\n'
    if 'result_prefix' in dct:
        result = dct['result_prefix']+'\n'+result
    if 'result_file' in dct:
        try:
            f=open(dct['result_file'],'w')
            f.write(result)
            f.close()
        except:
            print ('Cannot open: %s\n%s\n' % (dct['result_file'],result))
    else:
        print (result)

def getargs():
    dct = {}
    for i in range(1,len(sys.argv)):
        sides = sys.argv[i].split('=')
        if len(sides) == 2:
            dct[sides[0]] = sides[1]
    return dct

main()
'''
AllBoards = {}
b3 = '_________'
print('\nthis should be a draw in 9 moves')
CreateAllBoards(b3)
node3 = AllBoards[b3]
node3.print_me()
node3.print_layout()

AllBoards = {}
b1 = 'x_o_o___x'
print('x should win this one in 3 moves')
CreateAllBoards(b1)
node1 = AllBoards[b1]
node1.print_me()
node1.print_layout()

AllBoards = {}
b2 = 'x__xoxo__'
print('\no should win this one in 1 move')
CreateAllBoards(b2)
node2 = AllBoards[b2]
node2.print_me()
node2.print_layout()
'''
