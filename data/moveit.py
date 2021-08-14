#!/usr/bin/env python3

import os,sys,glob

#files = glob.glob('2021????/*')
files = glob.glob('2021????/*')
print('files=', len(files))
for f in files:
    dname = os.path.dirname(f)
    dr   = dname[:6]
    ndir = dname[:6] +'/'+ dname[6:8]
    base = os.path.basename(f)
    nname = ndir +'/'+ base
    print(f"file={f}  d={dname} nd={ndir}  b={base}")
    if not os.path.exists(dr): os.mkdir(dr)
    if not os.path.exists(ndir): os.mkdir(ndir)
    print(f"move {f} {nname}")
    os.rename(f, nname)

dirs = glob.glob('2021????')
for d in dirs:
    os.rmdir(d)

