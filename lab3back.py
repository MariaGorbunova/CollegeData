import requests
from bs4 import BeautifulSoup
import re
import json
import sqlite3

data = {}

page = requests.get('https://www.payscale.com/college-salary-report/best-schools-by-state/2-year-colleges/california'
                    '/page/1')
soup = BeautifulSoup(page.content, "lxml")

x = soup.find("script", id="__NEXT_DATA__")
#print(x)
#print(type(x))

#print(x.contents[0])

m = re.search('(\[.*?\])', x.contents[0])
data = [m.group(1)]
#print(type(data))
#print(data)

res = [json.loads(idx) for idx in data]


y = json.dumps(res)
print(y)
#print(res)
#print(type(res[0]))
#print(res[0])
#print(res[0][4])

#data = data.split('},{')
#print(data[0]+"}")

#y = json.loads(data[0]+"}")
#print(y['id'])
print("============")
#mydata = json.loads(x[0])
#print(mydata)


#for item in soup.select(""):
#    print(item.getText())
# with open('file.json', 'w') as fh:
#    json.dump(data, fh, indent=3)
