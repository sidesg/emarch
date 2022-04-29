#!/usr/local/bin/python3

"""
Creates individual txt files of transcriptions from cdliatf_unblocked
based on csv created by delimit_fonds.py.
"""

from pathlib import Path

with open("../fonds_info/fonds_pnums.txt") as infile:
    pnum_list = infile.read().split()

transc_hdir = Path("../atf/indiv_atf")

if not transc_hdir.exists():
    transc_hdir.mkdir()


print(f"{len(pnum_list)} p-numbers loaded")

with open("../cdli_data/cdliatf_unblocked.atf", "r") as infile:
    allatf = [line.rstrip('\n') for line in infile]

for pnum in pnum_list:
    transc_pth = Path(transc_hdir / (pnum + ".txt"))
    if not transc_pth.exists():
        ttest = min([l for l in allatf if '&' + pnum in l], default=0)
        if ttest != 0:
            tstart = allatf.index(ttest)
            tend = allatf.index(min(a for a in allatf if a == ''), tstart)
            tatf = '\n'.join(allatf[tstart:tend])
            with open(transc_pth, 'w') as outfile:
                outfile.write(tatf)