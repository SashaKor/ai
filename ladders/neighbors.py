#! /usr/bin/python3

import sys

def findNeighbors(infile, outfile):
    f = open(infile,'r').read().split('\n')
    o = open(outfile,'w')
    wordlst= wordList()
    dct= {}

    for word in f:
        cnt=0
        if len(word) != 0:
            dct[word]=[]
            for entry in wordlst:
                if len(entry)== len(word):
                    if len(set(word).intersection(set(entry)))== (len(word)-1):
                        posCnt=0
                        for i in range(0, len(entry)):
                            if word[i]==entry[i]:
                                posCnt+=1
                        if posCnt == (len(word)-1):
                            dct[word].append(entry)
                            cnt+=1
            o.write(word+","+str(cnt)+"\n")
    
    o.close()
    return dct #creation of dict as per assignment requirement   

#open standard word list and split by line
def wordList():
    wordlst = open("dictall.txt","r").read().split('\n')
    return wordlst

findNeighbors(sys.argv[1],sys.argv[2])
