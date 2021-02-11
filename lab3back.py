import requests
from bs4 import BeautifulSoup
import re
import json
import sqlite3



page = requests.get('https://www.payscale.com/college-salary-report/best-schools-by-state/2-year-colleges/california'
                    '/page/1')
soup = BeautifulSoup(page.content, "lxml")


test = soup.find()

mytable = soup.find("table", attrs={"class": "data-table"})
print(mytable)
headings = []
for item in mytable.select("th", attrs={"class": "csr-col--rank data-table__header data-table__header--active data-table__header--sortable"}):
    # remove any newlines and extra spaces from left and right
    print(item.getText())
    headings.append(item.getText().replace('\n', ' ').strip())
print("===========")
print(headings)
print("===========")

line = []
for item in mytable.find_all("tr", attrs={"class": "data-table__row"}):
    # remove any newlines and extra spaces from left and right
    #print(type(item))
    #print(item)
    #print(item.getText())
    #print(item.find_all("span", attrs={"class": "data-table__value"}))

    mydict = {}
    for i in item.find_all("td"):

        # print(i)
        mystr = i.getText().split(':')
        # convert to int if convertable
        mydict[mystr[0]] = mystr[1]

    #remove rank, high meaning and add the link
    line.append(mydict)
print("===========")
print(line)

'''
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