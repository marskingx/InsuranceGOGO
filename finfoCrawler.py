import requests
from bs4 import BeautifulSoup
from urllib.parse import unquote
import xlwt


class ProductBlock:
    def __init__(self, name, detailUrl):
        self.name = name
        self.detailUrl = detailUrl


urlRrefix = "https://finfo.tw/"
mainUrl = "inquired"
pageUrl = "?page="
productBlocks = []


# 爬取網頁
def getHtmlText(url):
    try:
        r = requests.get(url)
        r.raise_for_status()  # 如果狀態不是200, 引發異常
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return "發生異常"


# 取得要爬的網頁URL
def getCrawlerCompanyUrl():
    crawlerCompanyUrl = []
    soup = BeautifulSoup(getHtmlText(urlRrefix + mainUrl), 'html.parser')
    tags_div = soup.find_all(class_="insurers-block")

    for div in tags_div:
        url = urlRrefix + div.find("a").get('href')
        crawlerCompanyUrl.append(url)

    return crawlerCompanyUrl


# 取得商品頁數
def getPageCount(url):
    count = 0
    soup = BeautifulSoup(getHtmlText(url), 'html.parser')
    tags_span = soup.find_all(class_="page")

    for span in tags_span:
        count = count + 1

    count = count if count > 1 else 1
    return count


# 取得單頁商品區塊及細節連結
def getProductBlock(url):
    blocks = []
    soup = BeautifulSoup(getHtmlText(url), 'html.parser')
    tags_div = soup.find_all(class_="detail-product-card product-line")

    for div in tags_div:
        title = div.find(class_="title").text
        detailUrl = div.find(class_="link").get('href')
        detailUrl = urlRrefix + detailUrl
        detailUrl = unquote(detailUrl)
        productBlock = ProductBlock(title, detailUrl)
        blocks.append(productBlock)
    return blocks


# 寫入excel
def writeExcel(productBlocks):
    print("寫入excel")
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet('Finfo Worksheet', cell_overwrite_ok=True)
    worksheet.write(0, 0, '商品名稱')
    worksheet.write(0, 1, '商品細項網址')
    count = 1

    for productBlock in productBlocks:
        name = productBlock.name
        detailUrl = productBlock.detailUrl
        worksheet.write(count, 0, name)
        worksheet.write(count, 1, xlwt.Formula('HYPERLINK("' + detailUrl + '")'))
        count = count + 1

    workbook.save('Finfo.xls')


def main():
    # 取得要爬取的公司Url
    crawlerCompanyUrl = getCrawlerCompanyUrl()
    # 依URL 爬取
    for companyUrl in crawlerCompanyUrl:
        deocde = unquote(companyUrl).replace("https://finfo.tw//insurers/", "")
        print("正在爬取: " + deocde)
        # 確認每個公司要爬取的頁數
        page = getPageCount(companyUrl)
        # 依頁數爬取data
        for i in range(1, page + 1):
            print("共" + str(page) + "頁，正在爬取第" + str(i) + "頁")
            productUrl = companyUrl + pageUrl + str(i)
            blocks = getProductBlock(productUrl)
            for productBlock in blocks:
                productBlocks.append(productBlock)

    # 寫入excel
    writeExcel(productBlocks)


main()
