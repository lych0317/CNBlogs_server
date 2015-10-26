#!/usr/local/bin/python
# -*- coding:utf8 -*-
__author__ = 'liyc'

import urllib2
import re
from bs4 import BeautifulSoup

def search_blog_keyword_page(keyword, page="0"):

    url = "http://zzk.cnblogs.com/s?t=b&dateMin=2013-01-01"
    if keyword:
        url = url + "&w=" + keyword
    if page:
        url = url + "&p=" + page

    print url

    req = urllib2.Request(url)
    con = urllib2.urlopen(req)
    doc = con.read()
    con.close()

    soup = BeautifulSoup(doc, 'html.parser')
    searchItemArray = soup.find_all("div", attrs={"class": "searchItem"})

    itemArray = []

    for searchItem in searchItemArray:
        item = {}

        tag = searchItem.find(attrs={"class": "searchItemTitle"})
        if tag:
            href = tag.a.get("href")
            pattern = re.compile("/")
            match = pattern.split(href)[-1]
            if match:
                pattern = re.compile("\.")
                match = pattern.split(match)[0]
                if match:
                    pattern = re.compile("^\d*$")
                    match = pattern.match(match)
                    if match:
                        item["identifier"] = match.group()
                    else:
                        continue
            item["link"] = href

        tag = searchItem.find(attrs={"class": "searchItemTitle"})
        if tag:
            item["title"] = tag.a.text

        tag = searchItem.find(attrs={"class": "searchCon"})
        if tag:
            item["summary"] = tag.text.strip()

        tag = searchItem.find(attrs={"class": "searchItemInfo-userName"})
        if tag:
            author = {"uri": tag.a.get("href"), "name": tag.a.text, "avatar": ""}
            item["author"] = author

        tag = searchItem.find(attrs={"class": "searchItemInfo-publishDate"})
        if tag:
            item["publishDate"] = tag.text
            item["updateDate"] = tag.text

        pattern = re.compile("\d+")

        tag = searchItem.find(attrs={"class": "searchItemInfo-good"})
        if tag:
            good = tag.text
            match = pattern.search(good)
            if match:
                item["diggs"] = match.group()

        tag = searchItem.find(attrs={"class": "searchItemInfo-comments"})
        if tag:
            comments = tag.text
            match = pattern.search(comments)
            if match:
                item["comments"] = match.group()

        tag = searchItem.find(attrs={"class": "searchItemInfo-views"})
        if tag:
            views = tag.text
            match = pattern.search(views)
            if match:
                item["views"] = match.group()
        itemArray.append(item)

    return itemArray
