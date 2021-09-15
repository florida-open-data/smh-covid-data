#!/usr/bin/env python3

# convert HTML to text and json files
# maybe? download HTML if not already present
# Usage: python3 ./convert.py data/$dt/daily-update.html
#

import sys,os
import datetime

print("Convert Utility")
print(sys.argv)

assert len(sys.argv)==2, 'require single parameter: daily html file path'

#htmlfilename = sys.argv[1] + '.html'
htmlfilename = sys.argv[1]
basename = os.path.splitext(sys.argv[1])[0]
textfilename = basename + '.txt'
jsonfilename = basename + '.json'
csvfilename = basename + '.csv'

mystr = None


def download():
    import urllib.request
    link = "https://www.smh.com/Home/News-Events/Release/coronavirus-daily-news-update"
    fp = urllib.request.urlopen(link)
    mybytes = fp.read()
    mystr = mybytes.decode("utf8").strip()
    fp.close()
    print("lines: ", len(mystr))
    # save html file for testing/debug
    hfile = open(htmlfilename,'wb')
    hfile.write(mybytes)
    hfile.close()

def readhtml():
    hfile = open(htmlfilename,'rb')
    mybytes = hfile.read()
    hfile.close()
    #mystr = mybytes.decode("utf8",errors='strict').strip()
    mystr = mybytes.decode("utf8").strip()
    return mystr

print('html file: ', htmlfilename)
#if not os.path.exists(htmlfilename):
#    download()
#assert os.path.exists(htmlfilename), 'failed download of daily html file'
assert os.path.exists(htmlfilename), 'require daily html file'

mystr = readhtml()
#sys.exit(0)

# Parse HTML for raw text lines
import bs4
soup = bs4.BeautifulSoup(mystr, 'html.parser')
lines = soup.find("div", class_="main_content").find_all("p")
raw = []
for l in lines:
    for d in l.text.strip().split("\n"):
        if d is None or d=='': continue
        #print('DATA: >%s<' % d)
        raw.append(d)
print("raw data lines: ", len(raw))


# Parse HTML for date
sp = soup.find("div", class_="article details")
strings = sp.contents
s = strings[8] # get date like: Friday, July 16, 2021
info_date = str(s)
print('****  info_date: ', info_date)
parts = info_date.replace(',','').split()
mdy = ' '.join(parts[1:4])
#print('mdy=',mdy)
iso_date = datetime.datetime.strptime(mdy, "%B %d %Y").isoformat()
print('Info_Date: ', iso_date)



#
# Helper functions to return numbers within text lines
#

import re

def cleanText(s):
     ''' remove symbols, clean text '''
     s = re.sub(r'[*()%,:]', '', s)
     s = re.sub(r' +', ' ', s)
     s = s.strip()
     #logging.debug("clean str: %s", s)
     return s

def get_nums(r):
    parts = re.findall('(\d+\.?\d*)', cleanText(r))
    return parts
#     return [42, 69]

def get_one(r):
    return [ get_nums(r)[0] ]

def get_two(r):
    return get_nums(r)[:2]

def get_clean(r):
    s = cleanText(r)
    s = re.sub('\.', '', s)
    return [s]

def get_raw(r):
    return [r]

def get_rate(r):
    lst = get_nums(r)
    return lst[1:3]


# pattern, func, [schema fields, ...]
# Sep8: "COVID-positive patients total" became "COVID patients total", and "COVID-positive patients in ICU" became "COVID patients in ICU"
# Sep8: "Unvaccinated COVID-positive patients in the hospital" became "Unvaccinated COVID patients in the hospital"
# this was to reflect non-infectious patients still in hospital due to covid (see comments in source page HTML)
mapping = [
    {'p':"s patient census", 'f':get_one, 's':['total_patient'] },
    {'p':"COVID patients total", 'f':get_two, 's':['total_patient_today','total_patient_yesterday'] },
    {'p':"COVID-positive patients total", 'f':get_two, 's':['total_patient_today','total_patient_yesterday'] },
    {'p':"s ICU census", 'f':get_two, 's':['total_icu_today','total_icu_yesterday'] },
    {'p':"COVID-positive patients in ICU", 'f':get_two, 's':['covid_icu_today','covid_icu_yesterday'] },
    {'p':"COVID patients in ICU", 'f':get_two, 's':['covid_icu_today','covid_icu_yesterday'] },
    {'p':"Total hospital beds", 'f':get_one, 's':['total_beds'] },
    {'p':"ICU bed capacity", 'f':get_one, 's':['total_icu_beds'] },
    {'p':"7-Day SMH positivity rate", 'f':get_rate, 's':['positivity_rate','positivity_rate_last_week'] },
    {'p':"Unvaccinated COVID-positive patients in the hospital", 'f':get_one, 's':['percent_unvaccinated'] },
    {'p':"Unvaccinated COVID patients in the hospital", 'f':get_one, 's':['percent_unvaccinated'] },
    {'p':"Patients who have tested positive", 'f':get_one, 's':['total_test_positive'] },
    {'p':"Patients who have tested negative", 'f':get_one, 's':['total_test_negative'] },
    {'p':"through SMH systems since", 'f':get_clean, 's':['since_date'] },
    {'p':"hospitalized since outbreak began", 'f':get_two, 's':['cumm_patient_today','cumm_patient_yesterday'] },
    {'p':"Patients treated/discharged", 'f':get_two, 's':['cumm_patient_discharged_today','cumm_patient_discharged_yesterday'] },
    {'p':"Total hospital beds", 'f':get_one, 's':['total_beds'] },
    {'p':"Patient deaths", 'f':get_two, 's':['cumm_deaths_today','cumm_deaths_yesterday'] },
]

#
# Parse text lines for json schema field information
#

print('write text file: ', textfilename )
tfile = open(textfilename,'wb')
#tfile.write( ('info_date: '+(info_date.decode('utf8')+"\n")).encode('utf8') )
#tfile.write( ('info_date: '+(info_date).decode('utf8') ).encode('utf8') )
#tfile.write( ('info_date: '+info_date).encode('utf8') )
tfile.write( ('info_date: '+iso_date).encode('utf8') )
info = {}
for r in raw:
    print('raw: ', r)
    #tfile.write(r.encode('utf8')+"\n")
    tfile.write( (r+"\n").encode('utf8') )
    for m in mapping:
        if re.search(m['p'],r):
            print('got: ',r)
            lst =  (m['f'])(r)
            is_num = m['f'] not in [get_raw, get_clean]
            print('1: ', m['s'][0], ' = ', lst[0])
            if is_num: info[ m['s'][0] ] = float(lst[0])
            else: info[ m['s'][0] ] =  lst[0]
            if len(lst)>1:
                print('2: ', m['s'][1], ' = ', lst[1])
                #info[ m['s'][1] ] = float(lst[1])
                if is_num:
                    info[ m['s'][1] ] = float(lst[1])
                else:
                    info[ m['s'][1] ] =  lst[1]
tfile.close()
# include information date 
info['info_date'] = iso_date

#from pprint import pprint
#pprint(info) 
#print('info...', pprint(info) )

import json
print('write json file: ', jsonfilename )
print('json...', json.dumps(info) )
jfile = open(jsonfilename,'w')
jfile.write( json.dumps(info) )
jfile.close()

import csv
print('write csv file: ', csvfilename )
ks = info.keys()
print("csv keys: ", len(ks))
with open(csvfilename, mode='w') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=ks)
    writer.writeheader()
    writer.writerow(info)       

print("DONE!")

