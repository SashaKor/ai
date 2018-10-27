#! /usr/bin/python3
import sys

class PQueue:
    def __init__(self, is_min=True, compare=None, startlist=[]):
        self.size = 0
        self.datalist = [0]
        self.is_min = is_min

        if compare is not None:
            self.compare = compare
        else:
            self.compare = self._normal_cmp

        for element in startlist:
            self.push(element)


    def push(self,data):
        # if there's empty room at the end of the datalist (from previous pops), put it there, otherwise append it
        if len(self.datalist) <= self.size + 1:
            self.datalist.append(data)
        else:
            self.datalist[self.size + 1] = data
        self.size += 1

        # Bubble up from the data's current position
        self._bubble_up(self.size)

    def pop(self):
        if self.size == 0:
            return None

        if self.size == 1:
            self.size = 0
            return self.datalist[1]

        # save the answer
        answer = self.datalist[1]
        # Move last into root and bubble down from the top (position = 1)
        self.datalist[1] = self.datalist[self.size]
        self.size -= 1
        self._bubble_down(1)

        return answer

    def peek(self):
        # returns root
        if self.size== 0:
            return None
        return self.datalist[1]

    def size(self):
        return self.size

    def to_list(self):
        answer = []
        while True:
            best = self.pop()
            if best is not None:
                answer.append(best)
            else:
                return answer

    # This is the default comparison function
    def _normal_cmp(self,a,b):
        if a < b: return -1
        if a > b: return 1
        return 0

    def _swap(self,pos1,pos2):
        # swapper
        temp = self.datalist[pos1]
        self.datalist[pos1] = self.datalist[pos2]
        self.datalist[pos2] = temp

    def _bubble_up(self,position):
        # bubble up from the position if necessary
        child = position
        parent = position // 2
        while parent > 0:
            result = self.compare(self.datalist[child],self.datalist[parent])
            if self.is_min and result == -1:  # it's a min-queue and child is smaller than parent
                self._swap(parent,child)
            elif not self.is_min and result == 1:  # it's a max-queue and child is larger than parent
                self._swap(parent,child)
            else:
                break
            child = parent
            parent = child // 2

    def _bubble_down(self, position):
        # bubble down from position if necessary
        parent = position
        while True:
            left_child = parent * 2
            if left_child > self.size:
                return
            result_left = self.compare(self.datalist[left_child],self.datalist[parent])

            right_child = left_child + 1
            if right_child > self.size:
                # there's only the left child
                if self.is_min and result_left == -1:  # it's a min-queue and child is smaller than parent
                    self._swap(parent,left_child)
                elif not self.is_min and result_left == 1:  # it's a max-queue and child is larger than parent
                    self._swap(parent,left_child)
                else:
                    return
                parent = left_child
                continue

            # both children exist
            result_right = self.compare(self.datalist[right_child],self.datalist[parent])

            # decide which child to swap with, if we do end up swapping
            result_left_right = self.compare(self.datalist[left_child],self.datalist[right_child])
            if result_left_right == 0:
                swap_with = left_child # by convention
            elif self.is_min:
                if result_left_right == -1:  # it's a min_queue and left_child is smaller
                    swap_with = left_child
                else:                        # it's a min-queue and right_child is smaller
                    swap_with = right_child
            else:
                if result_left_right == -1:  # it's a max-queue and left_child is smaller
                    swap_with = right_child
                else:                        # it's a max-queue and right_child is smaller
                    swap_with = left_child

            # now compare the parent with the child we may swap with
            result_swap = self.compare(self.datalist[swap_with],self.datalist[parent])
            if self.is_min and result_swap == -1:  # it's a min-queue and child is smaller
                self._swap(swap_with,parent)
            elif not self.is_min and result_swap == 1:  # it's a max-queue and child is larger
                self._swap(swap_with,parent)
            else:
                return
            parent = swap_with


def findNeighbors(wlen):
    wordlst= wordList()
    #using list comp. to collect all word of wlen length
    mwords=[x for x in wordlst if len(x) == wlen]
    swords= set(mwords)
    dct={}
    for word in mwords:
        nb=[]
        for i in range(0,wlen):
            for char in set('abcdefghijklmnopqrstuvwxyz'):
                if char != word[i]:
                    #creating possible neighbors and seeing if they exist
                    nword = word[:i]+char+word[i+1:]
                    if nword in swords:
                        nb.append(nword)
        dct[word]=nb

    return dct #returns populated dictionary

#open standard word list and split by line
def wordList():
    wordlst = open("dictall.txt","r").read().strip().split('\n')
    return wordlst

class Node:
    def __init__(self,value,cost=0,path=[]):
        self.cost= cost #total cost to get to N from origin
        self.path= path #list of prev nodes
        self.value=value #word contained

    def NodeComparator(a,b):# pass in Nodes, return smaller cost, uninformed search
        if a.cost <= b.cost: return -1
        if a.cost > b.cost: return 1

    def __str__(self): return self.value

def getLadders(infile,outfile):
    #open input and return all pos. neighbors
    f = open(infile,'r').read().strip().split('\n')
    o = open(outfile, 'w')
    wlen = len((f[0].split(','))[0])
    dict = findNeighbors(wlen)

    for line in f:
        splt= line.split(',')
        origin= splt[0]#first word is origin
        target= splt[1]#second word is target
        originNode = Node(origin,0,[origin])  # origin now a node

        frontier = PQueue(True,Node.NodeComparator) # used to store frontier vals
        explored = set()

        frontier.push(originNode)#push first node to frontier
        currNode = originNode
        while frontier.size>0 and currNode.value != target: #if frontier is empty, expect sabotage
            currNode = frontier.pop()# pops next and bubbling happens
            if currNode.value == target:
                break
            elif tuple(currNode.value) in explored:
                continue
            else:
                explored.add(tuple(currNode.value))
                neighbors = dict[currNode.value]
                for nb in neighbors:
                    # if neighbor is in explored, ignore
                    if tuple(nb) in explored:
                        continue
                    # create a node for this neighbor
                    nbPath = currNode.path.copy() # make a copy of path(list) and update local copy
                    nbPath.append(nb)
                    nbNode = Node(nb, currNode.cost + 1, nbPath)
                    frontier.push(nbNode)

        o.write(','.join(currNode.path))
        o.write('\n')
    o.close()



        # a node is chosen from the frontier group
        #if node is target, then done searching
        #not but is laready in explored group: ignore the node, and go on to next best node in the frontier.
        #else: the node is removed from the frontier and put into explored group and:
        # each of node's neighbors is examined
getLadders(sys.argv[1],sys.argv[2])
