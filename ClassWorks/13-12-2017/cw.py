import requests
import time
from bs4 import BeautifulSoup


url = "http://quotes.toscrape.com"
r = requests.get(url=url)
soup = BeautifulSoup(r.content, "html.parser")
quotes = soup.select("div.quote")
quote = quotes[0]
text = quote.select_one("span.text").text
text = text[1:-1]

author = quote.select("small.author")
author_url = url + quote.select_one("span > a").get("href")

tags = quote.select(".tags > a")

next_page = soup.select("ul.pager")[0].select("li.next a")[0]

next_page_url = ""
has_next = True

while has_next:
    r = requests.get(url=url + next_page_url)
    print(r.status_code)
    soup = BeautifulSoup(r.content, "html.parser")
