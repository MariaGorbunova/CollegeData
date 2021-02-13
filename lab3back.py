# Maria Gorbunova
# lab3backend reads data from the website, saves it in json file.
# then creates sql db for the future use in frontend part

import requests
from bs4 import BeautifulSoup
import re
import json
import sqlite3

'''PART 1a'''
'''Reading data from the website and saving it in JSON file'''

listofLists = []
for i in range(1, 3):
    page = requests.get(
        'https://www.payscale.com/college-salary-report/best-schools-by-state/2-year-colleges/california'
        '/page/' + str(i))
    soup = BeautifulSoup(page.content, "lxml")
    # for item in soup.select("tr.data-table__row"):
    for row in soup.find_all("tr", attrs={"class": "data-table__row"}):
        mylist = []
        for idx, cell in enumerate(row.find_all("td")):
            # skip the rank and high meaning by the column idx
            if idx != 0 and idx != 5:
                mystr = cell.text.split(':')
                # TODO:convert to int if convertible; use regex to extract ints
                mylist.append(mystr[1])
        try:
            mylist.append("https://www.payscale.com" + row.a['href'])
        except TypeError:
            mylist.append("None")
        listofLists.append(mylist)
print(listofLists)
with open('data.json', 'w') as f:
    json.dump(listofLists, f, indent=3)

'''PART 1b'''
'''Reading data from the JSON file and saving it in SQLite3 DB file'''

with open('data.json', 'r') as fh:
    data = json.load(fh)
dataTuples = [tuple(item) for item in data]

conn = sqlite3.connect('lab3back.db')
cur = conn.cursor()
# TODO: create two tables for extra credit
cur.execute("DROP TABLE IF EXISTS CollegesDB")
cur.execute('''CREATE TABLE CollegesDB(             
                   name TEXT NOT NULL PRIMARY KEY,
                   sector TEXT,
                   earlyPay TEXT,
                   midPay TEXT,
                   stem TEXT,
                   url TEXT)
                   ''')
cur.executemany('INSERT INTO CollegesDB VALUES (?,?,?,?,?,?)', dataTuples)
conn.commit()
conn.close()

'''
# A different *REALLY COOL* approach, although it saves the whole table
# Pretty neat trick with json reading from a string that is a list of dictionaries

x = soup.find("script", id="__NEXT_DATA__")
print(x)
#print(type(x))

#print(x.contents[0])
m = re.search('(\[.*?\])', x.contents[0])
data = [m.group(1)]

print(len(data[0]))
print(data)

#print(type(data))
#print(data)

res = [json.loads(idx) for idx in data]

print(len(res[0]))
print(type(res[0][0]))

mylist = []
for idx in range(len(res[0])):
    mydict = res[0][idx]
    print(mydict)
    mylist.append(mydict)
print("Here")
print(mylist)

y = json.dumps(mylist)
print(y)
'''
