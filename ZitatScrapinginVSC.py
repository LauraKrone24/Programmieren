import requests 
from bs4 import BeautifulSoup
#import matplotlib.pyplot as plt

import pandas as pd
i=1
liste=[]
while i<=10:
    
    url = "http://quotes.toscrape.com/page/"+str(i)+"/"
    page= requests.get(url) 
    soup = BeautifulSoup(page.content,'html.parser')
    zitate=[]
    zitate = soup.findAll("div",attrs={"class":"quote"})
 
    for zitat in zitate:
        zitat_details= dict()
        zitat_details['text']=zitat.find("span",attrs={"class": "text"}).contents[0]
        zitat_details['autor']=zitat.find("small",attrs={"class":"author"}).contents[0]
        tags= [t.contents[0] for t in zitat.find_all("a",attrs={"class":"tag"})]
        zitat_details['tags']= tags
        zitat_details["länge"]=len(zitat_details['text'])
        zitat_details["anztag"]=len(tags)
        liste.append(zitat_details)
    i=i+1
   

df=pd.DataFrame(liste)
author_counts = df.groupby("autor").size();
#print(author_counts)

Autorenzahl=pd.DataFrame(author_counts)
Autorenzahl.columns= ['Anzahl']
print(Autorenzahl)
Autorenzahl=Autorenzahl.sort_values(by=['Anzahl'],ascending=[True])
print(Autorenzahl)
Autorenzahl.plot(figsize=(15,5))
Autorenzahl.plot.bar(figsize=(15,5))
print(df)
df.describe()
#plt.show()
