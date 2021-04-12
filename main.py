# -*- coding: utf-8 -*-


import csv
import os
from spider import Search
from _filter import Filter


def run(limit, KeyWd=None, Content=None, Summary=None, Author=None, Title=None, Theme=None, **kwargs):
    __filter = Filter(**kwargs)
    Subject = __filter.get_param().get("Subject")
    ArticleType = __filter.get_param().get("ArticleType")
    Order = __filter.get_param().get("Order")
    Year = __filter.get_param().get("Year")

    for p in range(1, limit + 1):
        Page = p
        search = Search(KeyWd=KeyWd, Content=Content, Summary=Summary, Author=Author, Title=Title, Theme=Theme,
                        Subject=Subject, ArticleType=ArticleType, Order=Order, Year=Year, Page=Page)
        result = search.parse()
        yield result


def save(content: list, file):
    if not file.endswith(".csv"):
        raise ValueError("file type must be csv!")
    if os.path.exists(file):
        f = open(file, "a+", newline="")
        csv_writer = csv.writer(f)
    else:
        f = open(file, "w", newline="")
        csv_writer = csv.writer(f)
        csv_writer.writerow(["标题", "作者", "摘要", "文献链接", "发表日期", "单位", "文献类型", "下载量", "引用量"])
    for i in content:
        title = i.items.get("title")
        abstract = i.items.get("abstract")
        author = i.items.get("author")
        href = i.items.get("href")
        date = i.items.get("date")
        department = i.items.get("department")
        article_type = i.items.get("article_type")
        download = i.items.get("download")
        cited = i.items.get("cited")

        csv_writer.writerow([title, author, abstract, href, date, department, article_type, download, cited])
    f.close()


if __name__ == "__main__":

    for c in run(limit=10, Content="MODIS"):

        save(c, r"C:\users\91481\desktop\test.csv")
