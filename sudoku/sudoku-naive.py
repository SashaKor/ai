#! /usr/bin/python3
import sys
import copy
import random

#Aleksandra Koroza
#Sudoku (naive) solver

class SuSolver:
    # default init reads provided file, assigns a default outfile name, and works with first unsolved board
    def __init__(self,infile="Sudoku-boards.txt",outfile="out.txt",name="Easy-NYTimes,unsolved"):
        self.inputfile=infile
        self.outputfile=outfile
        self.name= name
        self.initBoard= self.getInitState(self.getBoard(infile,name)) #a dictionary of the original state of the board
        self.currBoard= self.initBoard.copy() #current state of the board
        self.neighbors= self.getCliques() #dict of all neighbors
        self.backTrack= 0 #num times program backtracked

    # parses input file and returns appropriate board as a string
    def getBoard(self,infile,name):
        f = open(infile,'r').read().strip().split('\n')
        board="" #
        for line in range(0,len(f)): #number of lines
            if name in f[line]:
                for row in range(1,10):
                    board+=(f[line+row]+",")
                break
        return board

    #returns dict of initial state given a board
    #empty slots stored as underscores ("_")
    # key = cell, val = initial value
    def getInitState(self,strBoard):
        initBoard={}
        brd= strBoard.split(',').copy() #a list of all cells
        for i in range(0,81):
            if brd[i].isdigit():
                initBoard[i]=int(brd[i]) #to make sure I'm dealing with ints
            else:
                initBoard[i]= brd[i]
        return initBoard

    #returns dict of all possible neighbors of a certain cell
    #rows, columns, and box are neighbors
    #key = cell, val = set of all members of its 3 cliques w/o primary cell included (and no duplicates)
    def getCliques(self):
    # provided by Mr.Brooks
        Cliques=[[0,1,2,3,4,5,6,7,8],\
        [9,10,11,12,13,14,15,16,17],\
        [18,19,20,21,22,23,24,25,26],\
        [27,28,29,30,31,32,33,34,35],\
        [36,37,38,39,40,41,42,43,44],\
        [45,46,47,48,49,50,51,52,53],\
        [54,55,56,57,58,59,60,61,62],\
        [63,64,65,66,67,68,69,70,71],\
        [72,73,74,75,76,77,78,79,80,],\
        [0,9,18,27,36,45,54,63,72],\
        [1,10,19,28,37,46,55,64,73],\
        [2,11,20,29,38,47,56,65,74],\
        [3,12,21,30,39,48,57,66,75],\
        [4,13,22,31,40,49,58,67,76],\
        [5,14,23,32,41,50,59,68,77],\
        [6,15,24,33,42,51,60,69,78],\
        [7,16,25,34,43,52,61,70,79],\
        [8,17,26,35,44,53,62,71,80],\
        [0,1,2,9,10,11,18,19,20],\
        [3,4,5,12,13,14,21,22,23],\
        [6,7,8,15,16,17,24,25,26],\
        [27,28,29,36,37,38,45,46,47],\
        [30,31,32,39,40,41,48,49,50],\
        [33,34,35,42,43,44,51,52,53],\
        [54,55,56,63,64,65,72,73,74],\
        [57,58,59,66,67,68,75,76,77],\
        [60,61,62,69,70,71,78,79,80]
            ]

        neighbors= {}
        for cell in range(0,81):
            lst=[]
            for i in range(0,len(Cliques)):
                if cell in Cliques[i]:
                    for val in Cliques[i]:
                        lst.append(val)
            nb= set(lst)
            neighbors[cell]=nb
        return neighbors # I now have the addresses of all relevant cells, ie. those that can constrain that particular cell

    #solving sudoku board using recursive backtracking
    #cell 0 passed in initially
    #returns string answer
    def solve(self):
        return self.helpSolve(0)

    # solve() helper function
    #returns false if sudoku is not solved, true otherwise
    def helpSolve(self,cell):
        #if we have reached cell 81, we are done
        if (cell > 80):
            return True
        #if the cell is preset, ignore it and move on to next cell
        if (self.currBoard[cell]!= '_'):
            if (self.helpSolve(cell+1)):
                return True
        else:
            #generate random nums,assign to cell if works, and move on
            randList= [x for x in range(1,10)]
            random.shuffle(randList) #used to make sure that backtracking wont get stuck with same value
            for num in randList:
                if (not self.containedIn(num,cell)):
                    self.currBoard[cell]=num
                    #move to the next cell
                    if (self.helpSolve(cell+1)):
                        return True
                        #backtracking, try the whole thing over with a fresh set of random values
                    else:
                        self.currBoard[cell]='_'

        return False
    #output to outfile the name of the board followed by solution
    def getAnsBoard(self):
        o = open(self.outputfile,'w')
        o.write("name,"+self.name+"\n")
        self.solve()
        board=""
        for cell in self.currBoard:
            if len(board)%9==0:
                board+="\n"
            board+= (str(self.currBoard[cell])+",")
        o.write(board)
        o.close()

    #checks if a certain value is contained in row, column, box of current cell
    def containedIn(self,val,cell):
        for neighbor in self.neighbors[cell]: #fetches all relevant cells
            if self.currBoard[neighbor]== val:
                return True
        return False

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#testing area
solver= SuSolver(sys.argv[1],sys.argv[2],sys.argv[3])
solver.getAnsBoard()
