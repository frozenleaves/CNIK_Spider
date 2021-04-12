# -*- coding: utf-8 -*-

import sys
import requests
import io
import re
from bs4 import BeautifulSoup
from lxml import etree

# from _filter import Filter
# import os
# import csv

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')


class Item(object):
    def __init__(self, title, href, author, abstract=None, department=None, keywords=None, date=None, article_type=None,
                 download=None,
                 cited=None):
        self._items = {"title": title, "abstract": abstract, "href": href, "author": author, "department": department,
                       "date": date, "keywords": keywords, "article_type": article_type, "download": download,
                       "cited": cited}

    def set_abstract(self, abstract):
        self._items["abstract"] = abstract

    @property
    def items(self):
        return self._items

    def __str__(self):
        return str(self._items)

    def __repr__(self):
        return str(self._items)


class Search(object):
    def __init__(self, KeyWd=None, Content=None, Summary=None, Author=None, Title=None, Theme=None,
                 Subject=None, Year=None, ArticleType=None, Order=None, Page=1):
        if not (KeyWd or Content or Summary or Author or Title or Theme):
            raise ValueError("请输入搜索内容，关键字，主题，摘要，作者等至少一项！")
        self.url = 'http://search.cnki.com.cn/Search/ListResult'
        self.data = {
            'KeyWd': KeyWd,
            'Content': Content,
            'Summary': Summary,
            'Subject': Subject,
            'Year': Year,
            'ArticleType': ArticleType,
            'Order': Order,
            'Page': Page,
            'Author': Author,
            'Title': Title,
            'Theme': Theme,
            'searchType': 'MulityTermsSearch',
            'ReSearch': '',
            'ParamIsNullOrEmpty': 'false',
            'Islegal': 'false',
            'SearchFund': '',
            'Originate': '',
            'PublishTimeBegin': '',
            'PublishTimeEnd': '',
            'MapNumber': '',
            'Name': '',
            'Issn': '',
            'Cn': '',
            'Unit': '',
            'Public': '',
            'Boss': '',
            'FirstBoss': '',
            'Catalog': '',
            'Reference': '',
            'Speciality': '',
            'Type': '',
            'SpecialityCode': '',
            'UnitCode': '',
            'AuthorFilter': '',
            'BossCode': '',
            'Fund': '',
            'Level': '',
            'Elite': '',
            'Organization': '',
            'PageIndex': '',
            'ExcludeField': '',
            'ZtCode': '',
            'Smarts': '',
        }
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/53.0.2785.143 Safari/537.36 '
        }
        self.resp = requests.post(url=self.url, data=self.data, headers=self.headers)

        self.items = []

    def response(self):
        return self.resp

    def abstract(self, href):
        response = requests.get(url=href, headers=self.headers)
        tree = etree.HTML(response.text)
        _abstract = tree.xpath("/html/body/div[3]/div[2]/div[4]/text()")[1]
        line = re.split('\s+', _abstract)  # 将字符串i以全部空白字符为分割符，将其分割成一个字符列表
        content = ','.join(line)  # 将字符列表用','拼接成一个新字符串
        content = content.strip(',')  # 将新字符串尾部产生的','去掉
        # print(content)
        ret = ""
        for i in range(len(content)):
            if i != 0 and i % 50 == 0:
                ret = ret + "\n" + content[i]
            else:
                ret = ret + content[i]

        print(ret)
        return ret

    def item(self, title, href, author, department=None, date=None,
             article_type=None, cited=None, download=None, keywords=None):
        __item = Item(title=title, href=href, author=author, department=department, date=date,
                      article_type=article_type, cited=cited, download=download, keywords=keywords)

        __item.set_abstract(self.abstract(__item.items.get("href")))
        return __item

    def parse(self):
        items = []
        html = BeautifulSoup(self.response().content.decode(), features="lxml")
        td1 = html.select(".list-item")
        table = html.select(".re-table")
        trs = list(BeautifulSoup(str(table), features="lxml").find_all("tr"))
        for tr in trs[1::]:
            soup = BeautifulSoup(str(tr), features="lxml")
            tag_a = soup.find_all("a")
            tds = soup.find_all("td")
            title = tag_a[0].text
            href = "https:" + tag_a[0]['href']
            author = tag_a[1].text
            department = tag_a[2].text
            date = "".join(str(tds[4].text).split())
            article_type = tds[5].text
            cited = tds[6].text
            download = tds[7].text
            item = self.item(title=title, href=href, author=author, department=department, date=date,
                             article_type=article_type, cited=cited, download=download)
            items.append(item)
        # for j in td1:
        #     ps = j.find_all("p")
        #     # print(ps)
        #     title2 = ps[0].find("a").text
        #     href2 = "https:" + ps[0].find("a")["href"]
        #     author2 = [x.text for x in ps[2].find_all("a")]
        #     print(author2)
        #     department2 = ps[2].find_all("span")[2].text
        #     date2 = ps[2].find_all("span")[3].text
        #     # article_type2 = ps[2].find_all("span")[].text
        #     article_type2=None
        #     keywords2 = "".join(ps[3].text.split())
        #     cited2 = ps[4].select(".time2")[0].text
        #     download2 = ps[4].select(".time1")[0].text
        #     item2 = self.item(title=title2, href=href2, author=author2, department=department2, date=date2,
        #                       article_type=article_type2, cited=cited2, download=download2, keywords=keywords2)
        #     items.append(item2)

        return items


# def run(limit, KeyWd=None, Content=None, Summary=None, Author=None, Title=None, Theme=None, **kwargs):
#     __filter = Filter(**kwargs)
#     Subject = __filter.get_param().get("Subject")
#     ArticleType = __filter.get_param().get("ArticleType")
#     Order = __filter.get_param().get("Order")
#     Year = __filter.get_param().get("Year")
#
#     for p in range(1, limit + 1):
#         Page = p
#         search = Search(KeyWd=KeyWd, Content=Content, Summary=Summary, Author=Author, Title=Title, Theme=Theme,
#                         Subject=Subject, ArticleType=ArticleType, Order=Order, Year=Year, Page=Page)
#         result = search.parse()
#         yield result
#
#
# def save(content: list, file):
#     if not file.endswith(".csv"):
#         raise ValueError("file type must be csv!")
#     if os.path.exists(file):
#         f = open(file, "a+", newline="")
#         csv_writer = csv.writer(f)
#     else:
#         f = open(file, "w", newline="")
#         csv_writer = csv.writer(f)
#         csv_writer.writerow(["标题", "作者" , "摘要", "文献链接", "发表日期", "单位", "文献类型", "下载量", "引用量"])
#     for i in content:
#         title = i.items.get("title")
#         abstract = i.items.get("abstract")
#         author = i.items.get("author")
#         href = i.items.get("href")
#         date = i.items.get("date")
#         department = i.items.get("department")
#         article_type = i.items.get("article_type")
#         download = i.items.get("download")
#         cited = i.items.get("cited")
#
#         csv_writer.writerow([title, author, abstract, href, date, department, article_type, download, cited])
#     f.close()
#
#
# if __name__ == "__main__":
#     # r = Search(KeyWd="python")
#     # x = r.parse()
#     # for i in x:
#     #     print(i)
#     # print(len(x))
#     for c in run(limit=10, Content="植被指数变化"):
#         # print(c)
#         # print(type(c[0]))
#         save(c, r"C:\users\91481\desktop\植被指数变化.csv")
