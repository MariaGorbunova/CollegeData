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

# TODO: do a loop for two pages
page = requests.get('https://www.payscale.com/college-salary-report/best-schools-by-state/2-year-colleges/california'
                    '/page/1')
soup = BeautifulSoup(page.content, "lxml")

for item in soup.find_all("tr", attrs={"class": "data-table__row"}):
    # TODO: do i really need a dict? -no
    mydict = {}  # maybe use regular list?
    for i, cell in enumerate(item.find_all("td")):
        # skip the rank and high meaning by the column idx,
        # since it is said that the number and order of columns will never change
        if i != 0 and i != 5:
            mystr = cell.getText().split(':')
            # TODO:convert to int if convertible
            mydict[mystr[0]] = mystr[1]
    try:
        mydict["url"] = "https://www.payscale.com" + item.a['href']
    except TypeError:
        mydict["url"] = "None"
    listofLists.append(list(mydict.values()))

print(listofLists)

with open('data.json', 'w') as f:
    json.dump(listofLists, f, indent=3)

'''PART 1b'''

with open('data.json', 'r') as fh:
    data = json.load(fh)

dataTuples = [tuple(item) for item in data]
print(dataTuples)

conn = sqlite3.connect('lab3back.db')
cur = conn.cursor()

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

print(cur.execute('''SELECT * FROM CollegesDB'''))
results = cur.fetchall()
print(results)

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
