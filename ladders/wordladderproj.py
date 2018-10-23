#! /usr/bin/python3

import sys

#finds neighbors of given length
def findNeighbors(infile,outfile):
    f = open(infile,'r').read().split('\n')
    o = open(outfile,'w')
    wordlst= wordList()
    wlen= 4
    #using set comp. to collect all word of wlen length
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

    for entry in f:
        if len(entry) != 0:
            o.write(entry+','+ str(len(dct[entry]))+'\n')

    o.close()

#open standard word list and split by line
def wordList():
    wordlst = open("dictall.txt","r").read().strip().split('\n')
    return wordlst

findNeighbors(sys.argv[1],sys.argv[2])
