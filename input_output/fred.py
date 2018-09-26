#!/usr/bin/python3
# file takes two arguments from command line
import sys

def add(infile,outfile):
    infile= open(infile,'r')
    infile= f.read().split('\n')
    
    outfile= open(outfile,'w')
    for line in infile:
        
