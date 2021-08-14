#!/usr/bin/env python3

# combine daily json into single large json file
#
# TODO someday save json as dict with key by info_date (??)

import sys,os,glob,json,csv

print("Combine Utility")

outfile = 'smh_data.json'
tmpfile = 'smh_data_new.json'
csvfile = 'smh_data.csv'

full = []

def write_csv():
    print('write csv file: ', csvfile )
    newlist = sorted(full, key=lambda k: k['info_date']) 
    ks = list(newlist[3].keys())
    ks.append('percent_unvaccinated')
    print("csv keys: ", len(ks))
    print("csv key fieldnames: ", str(ks))
    print("csv key last: ", str(newlist[3]))
    with open(csvfile, mode='w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=ks)
        writer.writeheader()
        #newlist = sorted(full, key=lambda k: k['info_date']) 
        for d in newlist:
            d['info_date'] = d['info_date'].replace('T',' ') # hack for google sheets parsing
            writer.writerow(d)
    
def combine():
    # read single json files into full list
    print('read single files...')
    size = 0
    jfiles = glob.glob('data/*/*.json') + glob.glob('data/*/*/*.json')
    for f in jfiles:
        with open(f,'rb') as jf:
            s = jf.read().decode('utf8')
            j = json.loads(s)
            full.append(j)
            print('file %s json list size: %d ' % (f, len(j)) )
    size = len(full)
    print('total json list size: %d ' % (size) )

    # write full list
    print('write full tmp file... ', tmpfile)
    with open(tmpfile,'wb') as cf:
        newlist = sorted(full, key=lambda k: k['info_date'])
        s = json.dumps(newlist)
        cf.write(s.encode('utf8'))
    assert os.path.exists(tmpfile), 'tmpfile exists'
    
    #write csv file too
    write_csv()
    return size

def verify():
    # read new file, verify it works ok
    size = 0
    print('verify and release full tmp file... ', tmpfile)
    assert os.path.exists(tmpfile), 'tmpfile exists'
    with open(tmpfile,'rb') as cf:
        s = cf.read().decode('utf8')
        full = json.loads(s)
        print('new json list size: ', len(full))
        size = len(full)
    return size

def release():
    print('release file')
    os.remove(outfile)
    os.rename(tmpfile,outfile)

c = combine()
v = verify()
if c == v:
    release()
else:
    print("ERROR: combined (%d) not matching verify (%d)" % (c,v))

print("DONE!")

