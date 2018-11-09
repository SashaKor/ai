#! /usr/bin/python3
import sys

#Aleksandra Koroza
#Sudoku (naive) solver

def getAnswer(infile,outfile,name):
    f = open(infile,'r').read().strip().split('\n')
    o = open(outfile, 'w')
#parse through all lines, identify line with required board +9
# return necessary board
#row, column, and box clique make sure that none of the others dont have another
# 3. THose are your addresses for all of your cells
# read this in and create a new dictionary from this information
# key = position, and value= set(locations of all of its neighbors)
