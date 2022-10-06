from bs4 import BeautifulSoup
import pandas as pd
import requests
import matplotlib.pyplot as plt

quotes = []
authors = []
tags = []
page_count = 1


def fetch_data():
    global quotes
    global authors
    global tags
    global page_count

    url = "http://quotes.toscrape.com/page/" + str(page_count) + "/"
    print("Fetching data from", url + "...")
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    quote_text = soup.select(".quote .text")
    quote_authors = soup.select(".quote .author")
    quotes_raw = soup.find_all("div", class_="quote")

    quotes += [pt.get_text() for pt in quote_text]
    authors += [pt.get_text() for pt in quote_authors]

    for tags_raw in quotes_raw:
        tmp = [pt.get_text() for pt in tags_raw.select(".tags .tag")]
        tags.append(tmp)

    page_count += 1

    if not soup.find_all("li", class_="next"):
        return

    fetch_data()


fetch_data()
print()

df = pd.DataFrame(
    {
        "Zitat": quotes,
        "Autor": authors,
        "Tags": tags,
    }
)

quote_len = [len(q) for q in quotes]
tag_num = [len(n) for n in tags]

print(df)
print()

df_meta = pd.DataFrame(
    {
        "Quote length": quote_len,
        "Tag num": tag_num,
    }
)

print(df_meta)
print()

print("Zitatlänge Durchschnitt:", df_meta["Quote length"].mean())
print("Tag Anzahl Durchschnitt:", df_meta["Tag num"].mean())
print()
print(df["Autor"].value_counts())
print()

df["Autor"].value_counts().plot(kind="bar")
plt.show()
