#!/usr/local/bin/python3
from pathlib import Path
import re


pnum = input("Pnum: ")

pnum_path = Path("indiv_atf") / (pnum.strip() + '.txt')

if pnum_path:
    with open(pnum_path, 'r') as infile:
        atfstr = infile.read()
        junk = re.compile(r'[\[\]#<>?!\*\|]')
        numline = re.compile(r'[\d\']+\. (.+)')
        atfstr = junk.sub('', atfstr)
        atflist = [
            numline.search(line).group(1).strip() 
            for line in atfstr.split('\n') 
            if numline.match(line)
        ]
        print("\n" +'\n'.join(atflist) + "\n")
else:
    print(f"No transcription for {pnum}")