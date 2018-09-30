#! /usr/bin/python3

import math
import sys

#when elements are lists
def my_cmp(a,b):
    if len(a) < len(b): return -1
    if len(a) == len(b): return 0
    return 1

class Pqueue: #minheap

    def OrdComp(a,b): #ordinary comparison
        if a < b: return -1
        if a == b: return 0
        return 1

    def __init__(self, comparator = OrdComp):
        self.cmpfunc = comparator
        self.heap = ["DNE"]
        self.size = 0
        
    # parent: floor(index/2)
    # left: (2*index)
    # right: (2*index)+1
    # list populated started with 1st index
    def push(self, data): 
        if self.size == 0:
            self.heap.append(data) #start at index 1
            self.size+= 1
        else:
            self.heap.append(data)#add element to list
            self.size+= 1
            index= self.size
            
            while (index>1 and self.cmpfunc(self.heap[int(math.floor(index/2))],data))>0:#while parent is bigger than child...
                self.heap[index]= self.heap[int(math.floor(index/2))] #parent value
                index = int(math.floor(index/2)) #parent index
                self.heap[index]=data
                
    def pop(self): #pop smallest element or None if queue is empty
        def toHeap(index): #heapifies the removed index
            left= index*2
            right= (index*2)+1
            smaller= index
            
            if left<=self.size and right<=self.size:
                if self.cmpfunc(self.heap[left],self.heap[right])<0:
                    smaller=left
                else: 
                    smaller=right
            if left<= self.size and self.cmpfunc(self.heap[left],self.heap[smaller])<0:
                smaller=left
            if smaller != index:
                self.swap(self.heap,index,smaller)
                toHeap(smaller)
                
        if self.size ==0:
            return None
        root=self.heap[1]
        
        self.heap[1]=self.heap[self.size]
        del self.heap[self.size]
        self.size-=1
        
        toHeap(1)
        return root
    
            
    def peek(self): #peek at at the smallest element
        if len(self.heap)<2:
            return None
        else:
            return self.heap[1]
        
    def toList(self,pqueue):
        lst=[]
        numElems= pqueue.size
        if numElems==0:
            return []
        for i in range(numElems):
            lst.append(pqueue.pop())
        return lst
    
   
    def swap(self,lst,pos1,pos2):
        pos1Val=lst[pos1]
        pos2Val= lst[pos2]
        lst[pos1]= pos2Val
        lst[pos2]= pos1Val

def pqueueCheck(infile,outfile):
    freddy= Pqueue()
    f= open(infile,'r').read()
    lines= f.split('\n') #split by lines

    out= open(outfile,'w')

    for line in lines:
        spltLn= line.split(',')
        first= spltLn[0].lower()
        for elem in spltLn:
            elem.strip()
            if first == "push" and elem.isdigit():
                freddy.push(int(elem))
            elif first == "peek":
                out.write(str(freddy.peek())+('\n'))
            elif first == "pop":
                out.write(str(freddy.pop())+('\n'))
            elif first == "tolist":
                out.write(str(freddy.toList(freddy))+('\n'))
    out.close()

pqueueCheck(sys.argv[1],sys.argv[2])
'''
#testing 
Fred = Pqueue()
print(Fred.peek())
Fred.push(12)
Fred.push(3)
Fred.push(20)
Fred.push(1)
Fred.push(8)
Fred.push(0)
Fred.push(0)
Fred.push(3)
print(Fred.toList(Fred))
Fred.push([9])
Fred.push([98.33,2])
Fred.push(["Why not?","...because"])
Fred.push([2,"hello",[4,3]])
Fred.push([[4,3]])
Fred.push([[4,3]])
#print(Fred.peek())
#print (Fred.peek())
print("popping")
print(Fred.toList(Fred))
print (Fred.pop())
print(Fred.peek())
#print (Fred.pop())
#print (Fred.pop())
#print (Fred.pop())
#print (Fred.pop())
'''
