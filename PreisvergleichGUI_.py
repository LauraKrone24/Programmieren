from tkinter import *
from tkinter import ttk
import tkinter.scrolledtext as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import webbrowser
from functools import partial

def searchCallback(elem):
        global addVar, counter
        theValue = float(int(elem.split("|||")[1].strip("€").replace(",","").replace(".", ""))/100)
        addVar += theValue
        counter += 1
        return theValue


def getIdealo(searchQuery, filterSensitivity):
    global addVar, counter
    filterSensitivity = 10/filterSensitivity
    addVar = 0
    counter = 1
    r = requests.get(f"https://www.idealo.de/preisvergleich/MainSearchProductCategory.html?q={searchQuery}")
    soup = BeautifulSoup(r.text, "html.parser")
    ItemsList = soup.findAll("div", {"class":"offerList-item"})
    results = len(ItemsList)
    wholeList = []
    cleanList = []
    remList = []
    for i in ItemsList:
        a = i.find("a", {"class":"offerList-itemWrapper"})
        thePrice = a.find("div", {"class":"offerList-item-priceWrapper"}).find("div", {"class":"offerList-item-priceMin"}).text.replace(" ", "").strip("\nab\n\xa0€")+"€"
        theName = i.find("div", {"class":"offerList-item-description-title"}).text.strip("\n ")
        payload = "https://www.idealo.de" + a["href"] + "|||" + thePrice + "|||" + theName   
        wholeList.append(payload)
    wholeList.sort(key=searchCallback)
    avgPrice = round(addVar/counter, 2)
    limitPrice = avgPrice/filterSensitivity
    for item in wholeList:
        price = float(int(item.split("|||")[1].strip("€").replace(",","").replace(".", ""))/100)
        if float(price) < float(limitPrice):
            remList.append(item)
    for i in wholeList:
        if not i in remList:
            cleanList.append(i)
    links = []
    prices = []
    names = []
    for item in cleanList:
        payloadLink = item.split("|||")[0]
        payloadPrice = item.split("|||")[1]
        payloadName = item.split("|||")[2]
        links.append(payloadLink)
        prices.append(payloadPrice)
        names.append(payloadName)
    df = pd.DataFrame({"Link":links, "Preis":prices, "Name":names})
    return df



def getAmazon(searchQuery, filterSensitivity):
        global addVar, counter
        filterSensitivity = 10/filterSensitivity
        addVar = 0
        counter = 1
        url = "https://www.amazon.de/s?k="+searchQuery
        my_headers = {
            "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0"
        }
        page = requests.get(url, headers=my_headers)
        soup = BeautifulSoup(page.text,'html.parser')
        products = soup.findAll("div", {"data-component-type":"s-search-result"})
        links = []
        prices = []
        names = []
        ratings = []
        ratingVal = []
        ratingStrings = ["0-1", "1", "1-2", "2", "2-3", "3", "3-4", "4", "4-5", "5"]
        for item in products:
                if item.find("span", {"class":"a-price-whole"}) != None:
                    a = item.find("a", {"class":"a-link-normal a-text-normal"})
                    payloadLink = "https://www.amazon.de" + a["href"]
                    payloadPrice = item.find("span", {"class":"a-price-whole"}).text
                    payloadName = item.find("span", {"class":"a-size-medium a-color-base a-text-normal"}).text
                    try:
                        payloadRatings = item.find("span", {"class":"a-icon-alt"}).text
                        payloadRatingVal = float(payloadRatings.split(" ")[0].replace(",","."))
                    except:
                        payloadRatings = "No rating."
                        payloadRatingVal = "-"
                    links.append(payloadLink)
                    prices.append(payloadPrice)
                    names.append(payloadName)
                    ratings.append(payloadRatings)
                    ratingVal.append(payloadRatingVal)
                else:
                    continue
        artikelListe, preisListe, namenListe, ratingsListe, ratingValListe = list(links), list(prices), list(names), list(ratings), list(ratingVal)
        hybridListe = []
        for item in artikelListe:
            payload = f"{item}|||{preisListe[artikelListe.index(item)]}€|||{namenListe[artikelListe.index(item)]}|||{ratingsListe[artikelListe.index(item)]}|||{ratingValListe[artikelListe.index(item)]}"
            hybridListe.append(payload)
        hybridListe.sort(key=searchCallback)
        avgPrice = round(addVar/counter, 2)
        limitPrice = avgPrice/filterSensitivity
        remList = []
        for item in hybridListe:
                price = float(int(item.split("|||")[1].strip("€").replace(",","").replace(".",""))/100)
                if float(price) < float(limitPrice):
                        remList.append(item)
        cleanList = []
        for item in hybridListe:
                if not item in remList:
                        cleanList.append(item)
        artikelListe = []
        preisListe = []
        namenListe = []
        ratingsListe = []
        ratingValListe = []
        for item in cleanList:
            payloadArtikel = item.split("|||")[0]
            payloadPreis = item.split("|||")[1]
            payloadName = item.split("|||")[2]
            payloadRatings = item.split("|||")[3]
            payloadRatingsVal = item.split("|||")[4]
            artikelListe.append(payloadArtikel)
            preisListe.append(payloadPreis)
            namenListe.append(payloadName)
            ratingsListe.append(payloadRatings)
            ratingValListe.append(payloadRatingsVal)
        df = pd.DataFrame({"Link":artikelListe, "Preis":preisListe, "Name":namenListe, "Ratings":ratingsListe, "RatingVal":ratingValListe})
        return df


def getCyberport(searchQuery, filterSensitivity):
    suche=searchQuery
    global addVar, counter
    filterSensitivity = 10/filterSensitivity
    addVar = 0
    counter = 1
    url = "https://www.cyberport.de/tools/search-results.html?autosuggest=false&q="+suche
    my_headers = {
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0"
    }
    page = requests.get(url, headers=my_headers)



    soup = BeautifulSoup(page.content,'html.parser')
    hilfs = soup.find("div",attrs={"class":"serpArticleList productListView list"})
    linkh = []
    linkh = soup.findAll("a",attrs={"title":"Mehr Informationen zum Produkt"})
    x=hilfs.find("div",attrs={"class":"productsList"})["data-product-analyticsjson"]

    artikel=json.loads(x)
    Links= []
    for x in linkh:
        
        x=str(x).replace("<a class=\"head heading-level3\" href=\"","www.cyberport.de")
        a=str(x).split("\"")
        x=a[0]
       
        Links.append(x)
    linkliste=[] 
    i=0
    while i< (len(Links)/3):
        d= i*3
        linkliste.append(Links[d])
        i=i+1
        

    df=pd.DataFrame(artikel)
    i=0
    Preis= []
    for x in df["productGrossPrice"]:
        
        x=str(x).replace("","")
        a=str(x).split(",")
        x=a[0]
        x=x.replace("'","€")
        
        Preis.append(x)
    df['Preis']=Preis    
    df['Links']=linkliste
    liste = df[["productName","Preis","Links"]]
    liste.columns=["Bezeichnung","Preis","Link"]
    names = list(liste["Bezeichnung"].values)
    prices = list(liste["Preis"].values)
    links = list(liste["Link"].values)
    hybridList = []
    for i in links:
        payload = f"https://{i}|||{prices[links.index(i)].replace('.',',').strip('{€analyticsFormat€: €').strip('€')+'€'}|||{names[links.index(i)]}"
        hybridList.append(payload)
    hybridList.sort(key=searchCallback)
    avgPrice = round(addVar/counter, 2)
    limitPrice = avgPrice/filterSensitivity
    remList = []
    for item in hybridList:
        price = float(int(item.split("|||")[1].strip("€").replace(",","").replace(".",""))/100)
        if float(price) < float(limitPrice):
            remList.append(item)
    cleanList = []
    for item in hybridList:
        if not item in remList:
            cleanList.append(item)
    links = []
    prices = []
    names = []
    for item in cleanList:
        payloadLink = item.split("|||")[0]
        payloadPrice = item.split("|||")[1]
        payloadName = item.split("|||")[2]
        links.append(payloadLink)
        prices.append(payloadPrice)
        names.append(payloadName)
    df = pd.DataFrame({"Link":links, "Preis":prices, "Name":names})
    return df


def getBackMarket(searchQuery, filterSensitivity):
    global addVar, counter
    filterSensitivity = 10/filterSensitivity
    addVar = 0
    counter = 1
    url = f"https://www.backmarket.de/search?q={searchQuery}&ga_search={searchQuery}"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    products = soup.findAll("a", {"data-test":"product-thumb"})
    links = []
    prices = []
    names = []
    for item in products:
        payloadLink = "https://www.backmarket.de" + item["href"]
        payloadPrice = item.find("span", {"class":"_3OcKBk8D _2SrrvPwuOVjCyULC_FKjin"}).text
        payloadName = item.find("h2").text.replace("\n","")
        links.append(payloadLink)
        prices.append(payloadPrice)
        names.append(payloadName)
    hybridList = []
    for i in links:
        price = prices[links.index(i)].replace(" ","").strip("\n\xa0€")+"€"
        name = names[links.index(i)]
        payload = f"{i}|||{price}|||{name}"
        hybridList.append(payload)
    hybridList.sort(key=searchCallback)
    avgPrice = round(addVar/counter, 2)
    limitPrice = avgPrice/filterSensitivity
    remList = []
    for item in hybridList:
        price = float(int(item.split("|||")[1].strip("€").replace(",","").replace(".",""))/100)
        if float(price) < float(limitPrice):
            remList.append(item)
    cleanList = []
    for item in hybridList:
        if not item in remList:
            cleanList.append(item)
    links = []
    prices = []
    names = []
    for item in cleanList:
        payloadLink = item.split("|||")[0]
        payloadPrice = item.split("|||")[1]
        payloadName = item.split("|||")[2]
        links.append(payloadLink)
        prices.append(payloadPrice)
        names.append(payloadName)
    df = pd.DataFrame({"Link":links, "Preis":prices, "Name":names})
    return df


def getAll(searchQuery, filterSensitivity, minRange, maxRange):
        if filterSensitivity <= 0:
                filterSensitivity = 0.01
        productLinks = []
        productNames = []
        productPrices = []
        try:
                dfIdealo = getIdealo(searchQuery, filterSensitivity)
        except:
                dfIdealo = pd.DataFrame({"Link":[], "Preis":[], "Name":[]})
        try:
                dfBackMarket = getBackMarket(searchQuery, filterSensitivity)
        except:
                dfBackMarket = pd.DataFrame({"Link":[], "Preis":[], "Name":[]})
        try:
                dfAmazon = getAmazon(searchQuery, filterSensitivity)
        except:
                dfAmazon = pd.DataFrame({"Link":[], "Preis":[], "Name":[]})
        try:
                dfCyberport = getCyberport(searchQuery, filterSensitivity)
        except:
                dfCyberport = pd.DataFrame({"Link":[], "Preis":[], "Name":[]})
        productLinks += list(dfIdealo["Link"].values) + list(dfBackMarket["Link"].values) + list(dfAmazon["Link"].values) + list(dfCyberport["Link"].values)
        productNames += list(dfIdealo["Name"].values) + list(dfBackMarket["Name"].values) + list(dfAmazon["Name"].values) + list(dfCyberport["Name"].values)
        productPrices += list(dfIdealo["Preis"].values) + list(dfBackMarket["Preis"].values) + list(dfAmazon["Preis"].values) + list(dfCyberport["Preis"].values)
        hybridList = []
        for i in productLinks:
                price = productPrices[productLinks.index(i)]
                name = productNames[productLinks.index(i)]
                payload = f"{i}|||{price}|||{name}"
                hybridList.append(payload)
        hybridList.sort(key=searchCallback)
        keepList = []
        for item in hybridList:
                price = float(int(item.split("|||")[1].strip("€").replace(",","").replace(".",""))/100)
                if price < maxRange and price > minRange:
                        keepList.append(item)
        cleanList = []
        for item in hybridList:
                if item in keepList:
                    cleanList.append(item)
        links = []
        prices = []
        names = []
        for item in cleanList:
                payloadLink = item.split("|||")[0]
                payloadPrice = item.split("|||")[1]
                payloadName = item.split("|||")[2]
                links.append(payloadLink)
                prices.append(payloadPrice)
                names.append(payloadName)
        df = pd.DataFrame({"Link":links, "Preis":prices, "Name":names})

        return df

    

Fenster = Tk()
Fenster.title("Preisvergleich")
Fenster.resizable(0, 0)
Fenster.geometry('1000x700')
Fenster.config(bg="#EAFDF8")
schriftfarbe= "Black"


def zeigeDaten(dataframe):
        theRow = 10
        thePady = (20, 0)
        thePadx = (200, 0)
        strLength = 35
        linkLength = 50
        linkLabel.grid(row=theRow, padx=(25,0), column=3, pady=thePady)
        namenLabel.grid(row=theRow, padx=(50,0), column=2, pady=thePady)
        preisLabel.grid(row=theRow, padx=(20,0), column=1, pady=thePady)
        for item in range(1,len(dataframe.index)):
                name = dataframe.iloc[item, 2]
                preis = dataframe.iloc[item, 1]
                link = dataframe.iloc[item, 0]
                newLink = link
                if len(link) > linkLength:
                        newLink = f"{link[:(linkLength-3)]}..."
                if len(name) > strLength:
                        name = f"{name[:(strLength-3)]}..."
                rowOffset = (1*item)
                Label(second_frame, text=name, fg=schriftfarbe, bg="#EAFDF8").grid(row=theRow+rowOffset, padx=(50,0), column=2, pady=40)
                Label(second_frame, text=preis, fg=schriftfarbe, bg="#EAFDF8").grid(row=theRow+rowOffset, padx=(20,0), column=1, pady=40)
                Button(second_frame, text=newLink, fg=schriftfarbe, bg="#EAFDF8", command=partial(webbrowser.open, link)).grid(row=theRow+rowOffset, padx=(50,0), column=3, pady=40)
        main_frame.place(anchor="center", rely=0.6, relx=0.4)
        #main_frame.pack(side=LEFT, fill=BOTH, expand=1)
        my_canvas.pack(side=LEFT, fill=BOTH, expand=1)
        #my_canvas.place(anchor="n", y=200, relx=0.4)
        my_scrollbar.pack(side=RIGHT, fill=Y)
        my_canvas.configure(yscrollcommand=my_scrollbar.set)
        my_canvas.bind("<Configure>", lambda e: my_canvas.configure(scrollregion = my_canvas.bbox("all")))
        my_canvas.create_window((0,0), window=second_frame, anchor="nw")
        
        
        

def suchstart():
    home()
    shortcut1_button.place_forget()
    shortcut2_button.place_forget()
    shortcut3_button.place_forget()
    shortcut4_button.place_forget()

    handy_label.place_forget()
    tablet_label.place_forget()
    Laptop_label.place_forget()
    kopfhörer_label.place_forget()
    home_button.place(x=800, y=600, width= 190, height= 30)
    
    suche = str(eingabe.get())
    filter_sens = int(sensivität.get())
    minpreis = int(minpreis_scale.get())
    maxpreis = int(maxpreis_scale.get())

    print(minpreis)
    print(maxpreis)
    print(filter_sens)
    print(suche)
    
    if not len(suche) <= 0:
        err_label.place_forget()
        theProducts = getAll(suche, filter_sens, minpreis, maxpreis)
        zeigeDaten(theProducts)
    else:
        err_label.place(anchor="center", relx=0.5, rely=0.3)

def handy():
    eingabe.delete(0,END)
    eingabe.insert(0,"Handy")
    suchstart()
    

def tablet():
    eingabe.delete(0,END)
    eingabe.insert(0,"Tablet")
    suchstart()

def laptop():
    eingabe.delete(0,END)
    eingabe.insert(0,"Laptop")
    suchstart()

def kopfhörer():
    eingabe.delete(0,END)
    eingabe.insert(0,"Headset")
    suchstart()

def home():
    global my_canvas
    global my_scrollbar
    global main_frame
    global second_frame
    home_button.place_forget()
    my_canvas.pack_forget()
    err_label.place_forget()
    my_scrollbar.pack_forget()
    main_frame.place_forget()
    shortcut1_button.place(x=50, y=250, width=150, height=150) 
    shortcut2_button.place(x=248, y=250, width=150, height=150)
    shortcut3_button.place(x=446, y=250, width=150, height=150) 
    shortcut4_button.place(x=644, y=250, width=150, height=150)

    handy_label.place(x=75, y=420, width=100, height = 30)
    tablet_label.place(x=273, y=420, width=100, height = 30)
    Laptop_label.place(x=471, y=420, width=100, height = 30)
    kopfhörer_label.place(x=669, y=420, width=100, height = 30)
    main_frame = Frame(Fenster, bg="#EAFDF8")
    my_canvas = Canvas(main_frame, width=710, height=400, bg="#EAFDF8", highlightbackground="black")
    my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
    second_frame = Frame(my_canvas, bg="#EAFDF8")


# überschrift 
title_label= Label(master= Fenster, text="Wilkommen im Preisvergleichsprogramm", bg="#9FA0FF", fg=schriftfarbe)
title_label.place(x=0, y=30, width =1000, height= 40)
title_label.config(font=("Arial Nova",22))

untertitle_label= Label(master= Fenster, text= "Vergleiche die Preise verschiedener Seiten um das beste Angebot für DICH zu finden ", bg="#9FA0FF", fg=schriftfarbe )
untertitle_label.place(x=0, y=85, width = 1000, height= 20)
untertitle_label.config(font=("Arial Nova",12))

#Suchleiste
text1_label= Label(master= Fenster, text="  Suche:",bg="#9B9ECE",fg=schriftfarbe )
text1_label.place(x=50,y=150, width= 200, height= 30)
text1_label.config(font=("Arial Nova",16))

eingabe = Entry(master= Fenster, bg= 'white', text= "Nach welchem Produkt würden sie gerne suchen ?", fg=schriftfarbe)
eingabe.place(x=250, y=150, width=544, height=30 )
eingabe.config(font=("Arial Nova",12))

bestätigen = Button(master= Fenster, bg="white", text='Suche starten',command=suchstart, fg=schriftfarbe)
bestätigen.place(x=810, y=145, width=140, height=40 )
bestätigen.config(font=("Arial Nova",16))

#Filtersensivität
filter_label= Label(master = Fenster, text= "Filtersensivität", fg = schriftfarbe, bg="#9B9ECE")
filter_label.place(x=810, y=250, width=140, height=30 )
filter_label.config(font=("Arial Nova",14))

sensivität= Spinbox(master= Fenster, from_= 0, to= 15 )
sensivität.place(x=875, y= 285, width= 75, height= 30)

#Preisrange
preis_label= Label(master = Fenster, text= "Preisrange", fg = schriftfarbe, bg="#9B9ECE")
preis_label.place(x=810, y=330, width=140, height=30 )
preis_label.config(font=("Arial Nova",14))

minpreis_label= Label(master = Fenster, text= "Von:", fg = schriftfarbe, bg="#9B9ECE")
minpreis_label.place(x=890, y=370, width=60, height=30 )
minpreis_label.config(font=("Arial Nova",12))

minpreis_scale= Scale(master= Fenster, from_=0, to=2000, resolution= 10, orient= HORIZONTAL)
minpreis_scale.place(x=810, y=410, width= 140, height= 30)

maxpreis_label= Label(master = Fenster, text= "Bis:", fg = schriftfarbe, bg="#9B9ECE")
maxpreis_label.place(x=890, y=450, width=60, height=30 )
maxpreis_label.config(font=("Arial Nova",12))

maxpreis_scale= Scale(master= Fenster, from_=0, to=2000, resolution= 10, orient= HORIZONTAL)
maxpreis_scale.place(x=810, y=490,width=140, height= 30)
maxpreis_scale.set(5000)

#Homedashboard

    #Handy Button 
Bild1 =PhotoImage(file="Handy.png",width= 110, height= 110 ) 
shortcut1_button = Button(master = Fenster, bg="white", image= Bild1, command = handy)
shortcut1_button.place(x=50, y=250, width=150, height=150) 

handy_label= Label(master = Fenster, text= "Handy", fg=schriftfarbe, bg="#9B9ECE")
handy_label.place(x=75, y=420, width=100, height = 30)
handy_label.config(font=("Arial Nova",12))
    
    #Tablet Button 
Bild2 =PhotoImage(file="Tablet.png",width= 110, height= 110 ) 
shortcut2_button = Button(master = Fenster, bg="white", image= Bild2, command = tablet )
shortcut2_button.place(x=248, y=250, width=150, height=150)

tablet_label= Label(master = Fenster, text= "Tablet", fg=schriftfarbe, bg="#9B9ECE")
tablet_label.place(x=273, y=420, width=100, height = 30)
tablet_label.config(font=("Arial Nova",12))

    #Laptop Button 
Bild3 =PhotoImage(file="Laptop.png",width= 110, height= 110 ) 
shortcut3_button = Button(master = Fenster, bg="white", image= Bild3, command = laptop )
shortcut3_button.place(x=446, y=250, width=150, height=150) 

Laptop_label= Label(master = Fenster, text= "Laptop", fg=schriftfarbe, bg="#9B9ECE")
Laptop_label.place(x=471, y=420, width=100, height = 30)
Laptop_label.config(font=("Arial Nova",12))

    #Kopfhörer Button 
Bild4 =PhotoImage(file="Kopfhörer.png",width= 110, height= 110 ) 
shortcut4_button = Button(master = Fenster, bg="white", image= Bild4, command = kopfhörer )
shortcut4_button.place(x=644, y=250, width=150, height=150)

kopfhörer_label= Label(master = Fenster, text= "Kopfhörer", fg=schriftfarbe, bg="#9B9ECE")
kopfhörer_label.place(x=669, y=420, width=100, height = 30)
kopfhörer_label.config(font=("Arial Nova",12))

#Homebutton 
home_button = Button(master = Fenster, bg="white", text="Zurück zum Homemenu", command = home )

#Error Label
err_label = Label(fg="Red", bg="#EAFDF8", text="Bitte gebe ein Produkt an")

#Main Frame
main_frame = Frame(Fenster, bg="#EAFDF8")

#Widgets Canvas
my_canvas = Canvas(main_frame, width=710, height=400, bg="#EAFDF8", highlightbackground="black")

#Scrollbar
my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)


#Configure Canvas



#another Frame
second_frame = Frame(my_canvas, bg="#EAFDF8")

#add frame to window


#Tabellen Label
namenLabel = Label(second_frame, text="Bezeichnung", fg=schriftfarbe, bg="#EAFDF8")
linkLabel = Label(second_frame, text="Link", fg=schriftfarbe, bg="#EAFDF8")
preisLabel = Label(second_frame, text="Preis", fg=schriftfarbe, bg="#EAFDF8")


# Ausgabefeld 



  
# Inserting Text which is read only


Fenster.mainloop()
