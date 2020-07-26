import requests
from bs4 import BeautifulSoup
from urllib.parse import unquote
import xlwt
import io
import time


def sleeptime(hour, min, sec):
    return hour * 3600 + min * 60 + sec


tStart = time.time()  # 計時開始

r = requests.get("https://travel.ettoday.net/category/%E6%A1%83%E5%9C%92/")
soup = BeautifulSoup(r.text, "html.parser")

#print(soup.prettify())  #輸出排版後的HTML內容

result = soup.find_all("h3", itemprop="headline", limit=1)
print(result)

result = soup.find_all(["h3", "p"], limit=2)
print(result)