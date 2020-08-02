import bs4
import requests
from bs4 import BeautifulSoup
from urllib.parse import unquote
import xlwt
import io
import time

# class ProductBlock:
#     def __init__(self, company, detailUrl):
#         self.company = company
#         self.detailUrl = detailUrl


CompanyID = requests.get("https://ins-info.ib.gov.tw/customer/Info4-18.aspx?UID=28428384")
AIInsurance = bs4.BeautifulSoup(CompanyID.text, "html.parser")

companyID = AIInsurance.find("span", id="ctl00_MainContent_lbCompanyName")  # 尋找保險公司的名稱
print(companyID.text)

UpdateTime = bs4.BeautifulSoup(CompanyID.text, "html.parser")
UpdateTimes = AIInsurance.find("span", id="ctl00_MainContent_lblQyDate")  # 資料更新的時間
print(UpdateTimes.text)

RBC = bs4.BeautifulSoup(CompanyID.text, "html.parser")
RBCs = AIInsurance.find_all("tr", class_="tb3", )  # 取得公司的RBC資料
for tb3 in RBCs:
    if tb3 is not None:
        print(tb3.text)
