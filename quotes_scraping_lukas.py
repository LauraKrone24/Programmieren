# %%
from bs4.element import Tag
import requests
import bs4
import pandas


def getPageDoc(index) -> bs4.BeautifulSoup:
    html = requests.get(f"http://quotes.toscrape.com/page/{index + 1}/").text
    return bs4.BeautifulSoup(html, "html.parser")


quotes = []

pageIndex = 0
hasNextButton = True
while hasNextButton:
    doc = getPageDoc(pageIndex)

    ele: Tag
    for ele in doc.select(".quote"):
        quote = dict()

        quote["text"] = ele.select_one(".text").text.replace("“", "").replace("”", "")
        quote["text_len"] = len(quote["text"])
        quote["author"] = ele.select_one(".author").text
        quote["tags"] = [x.text for x in ele.select_one(".tags").select(".tag")]
        quote["tags_len"] = len(quote["tags"])

        quotes.append(quote)

    print(f"Page {pageIndex + 1}")

    pageIndex += 1

    if doc.select_one(".next") == None:
        hasNextButton = False

print("Ready!")
# %%
data = pandas.DataFrame(quotes)

print(f"Durchschnittliche Länge: {data['text_len'].mean()}")

print(f"Durchschnittliche tags: {data['tags_len'].mean()}")

print(f"Meist zitiert: {data['author'].mode()[0]}")

print("Am wenigsten zitiert:")
author_frame = pandas.DataFrame(data['author'].value_counts())
print(author_frame[author_frame["author"] == 1])

author_frame.plot.bar(figsize=(10, 3))
# %%
