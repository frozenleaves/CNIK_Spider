# -*- coding: utf-8 -*-
import requests
import io
from bs4 import BeautifulSoup
from lxml import etree

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
}
url = 'https://cdmd.cnki.com.cn/Article/CDMD-10445-1019095657.htm'
response = requests.get(url=url, headers=headers)


tree = etree.HTML(response.text)

# print(list(soup.find("strong").parents))

print(tree.xpath("/html/body/div[3]/div[2]/div[4]/text()")[1])