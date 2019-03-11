from bs4 import BeautifulSoup
import requests
import pandas as pd
from os import listdir
from os.path import isfile, join
import time

mypath = './dataset/'
files = [mypath+str(f) for f in listdir(mypath) if isfile(join(mypath,f))]
urlSet = set()
urlSetD = set()
urls = []
baseUrl = "https://en.wikipedia.org"

if len(files) == 0:
    print('Starting from fresh...')
    urlSet.add('/wiki/Main_Page')
    urls.append('/wiki/Main_Page')
else:
	print('Restoring state...')
	for f in files:
		fin = open(f,'r')
		for l in fin.readlines():
			l = l.strip()
			l = l.replace(baseUrl,"")
			url = l.split(' ')
			urlSet.add(url[0])
			urlSetD.add(url[1])
	urls = list(urlSetD-urlSet)

col = ['src','dest']
print('Starting mining...')
for url in urls:
    if url in urlSet:
        pass
    print("Processing "+url+" ... ",end="")
    urlDS = pd.DataFrame(columns=col)
    urls.remove(url)
    urlSet.add(url)
    r = requests.get(baseUrl+url)
    html = r.text
    soup = BeautifulSoup(html,features="html.parser")
    for link in soup.findAll("a"):
        x = str(link.get("href"))
        x = x.replace('\"','')
        if "/wiki/" in x and x.startswith("/wiki/") and ":" not in x:
            urls.append(x)
            s = baseUrl+url
            d = baseUrl+x
            tmp = pd.DataFrame([[s,d]],columns=col)
            urlDS = urlDS.append(tmp,ignore_index=True)
    urlDS.drop_duplicates(keep=False, inplace=True)
    name = url.replace('/wiki/','')
    name = name.replace('/',':')
    fileName = mypath+""+name+".csv"
    urlDS.to_csv(fileName,sep=" ",header=False,index=False,encoding="utf-8")
    print("Saved\n",end="")
