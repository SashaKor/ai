#! /usr/bin/python3

import sys

def main():
    infile = open(sys.argv[1], 'r')
    infile = infile.read().split('\n')# infile is now a list of lines
    outfile = open(sys.argv[2], 'w')

    for line in infile:
        splt = line.split(',')
        cnt = 0
        for elem in splt:
            elem = elem.strip()# stripping leading / trailing spaces
            if elem.isdigit() and int(elem) > 0:
                cnt += int(elem)
        if cnt != 0:
            outfile.write(str(cnt) + "\n")

main()
