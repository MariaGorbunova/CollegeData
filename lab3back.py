# Maria Gorbunova
# lab3backend reads data from the website, saves it in json file.
# then creates sql db for the future use in frontend part

import requests
from bs4 import BeautifulSoup
import re
import json
import sqlite3

LINK = 'https://www.payscale.com/college-salary-report/best-schools-by-state/2-year-colleges/california/page/'

"""PART 1a"""


def writeJSON():
    """Reading data from the website and saving it in JSON file"""
    listofLists = []
    try:
        for i in range(1, 3):
            page = requests.get(LINK + str(i))
            soup = BeautifulSoup(page.content, "lxml")
            # for item in soup.select("tr.data-table__row"):
            for row in soup.find_all("tr", attrs={"class": "data-table__row"}):
                mylist = []
                for idx, cell in enumerate(row.find_all("td")):
                    # skip the rank and high meaning by the column idx
                    if idx != 0 and idx != 5:
                        mystr = cell.text.split(':')[1]
                        # convert to int if convertible; use regex to extract ints
                        if re.search('\d', mystr):
                            x = re.findall('[0-9]+', mystr)
                            mystr = int(''.join(x))
                        mylist.append(mystr)
                try:
                    mylist.append("https://www.payscale.com" + row.a['href'])
                except TypeError:
                    mylist.append("None")
                listofLists.append(mylist)
    # Request Error Handling
    except requests.exceptions.HTTPError as e:
        print("HTTP Error:", e)
    except requests.exceptions.ConnectionError as e:
        print("Error Connecting:", e)
    except requests.exceptions.Timeout as e:
        print("Timeout Error:", e)
    except requests.exceptions.RequestException as e:
        print("Request exception:", e)

    # print(listofLists)
    with open('data.json', 'w') as f:
        json.dump(listofLists, f, indent=3)


"""PART 1b"""


def createDB():
    """Reading data from the JSON file and saving it in SQLite3 DB file"""
    with open('data.json', 'r') as fh:
        data = json.load(fh)
    conn = sqlite3.connect('lab3back.db')
    cur = conn.cursor()
    collegeTuples = [tuple(item) for item in data]
    # EC: create two tables for extra credit
    sectorTuples = set([item[1] for item in data])
    cur.execute("DROP TABLE IF EXISTS SectorsDB")
    cur.execute('''CREATE TABLE SectorsDB( sector_id INTEGER NOT NULL PRIMARY KEY UNIQUE,
                   sector TEXT UNIQUE ON CONFLICT IGNORE )''')
    for item in sectorTuples:
        cur.execute('''INSERT INTO SectorsDB (sector) VALUES (?)''', (item,))

    cur.execute("DROP TABLE IF EXISTS CollegesDB")
    cur.execute('''CREATE TABLE CollegesDB(             
                           name TEXT NOT NULL PRIMARY KEY,
                           sector_id INTEGER,
                           earlyPay INTEGER,
                           midPay INTEGER,
                           stem INTEGER,
                           url TEXT) ''')

    for college in collegeTuples:
        cur.execute('SELECT sector_id FROM SectorsDB WHERE sector = ? ', (college[1],))
        sector_id = cur.fetchone()[0]
        cur.execute('''INSERT INTO CollegesDB
                (name, sector_id, earlyPay, midPay, stem, url) 
                VALUES ( ?, ?, ?, ?, ?, ? )''', (college[0], sector_id, college[2], college[3], college[4], college[5]))
    """
    #initial working code
    cur.execute("DROP TABLE IF EXISTS CollegesDB")
    cur.execute('''CREATE TABLE CollegesDB(             
                       name TEXT NOT NULL PRIMARY KEY,
                       sector TEXT,
                       earlyPay INTEGER,
                       midPay INTEGER,
                       stem INTEGER,
                       url TEXT)
                       ''')
    cur.executemany('INSERT INTO CollegesDB VALUES (?,?,?,?,?,?)', collegeTuples)
    """
    conn.commit()
    conn.close()


writeJSON()
createDB()

'''
# A different *REALLY COOL* approach, although it saves the whole table
# Pretty neat trick with json reading from a string that is a list of dictionaries

x = soup.find("script", id="__NEXT_DATA__")
m = re.search('(\[.*?\])', x.contents[0])
data = [m.group(1)]
res = [json.loads(idx) for idx in data]
mylist = []
for idx in range(len(res[0])):
    mydict = res[0][idx]
    mylist.append(mydict)
y = json.dumps(mylist)
print(y)
'''
