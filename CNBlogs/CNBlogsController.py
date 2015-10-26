#!/usr/local/bin/python
# -*- coding:utf8 -*-
__author__ = 'liyc'

from flask import Flask
from flask import request
from flask import Response
import json
from Protocol import SearchBlogProtocol
from Protocol import SearchNewsProtocol

app = Flask(__name__)

@app.route('/search/blog', methods=['GET'])
def search_blog():
    keyword = request.args.get('keyword', '')
    page = request.args.get('page', '')
    print keyword
    print page

    data = SearchBlogProtocol.search_blog_keyword_page(keyword, page)
    print data
    if data:
        resData = {"status": 0, "data": data}
        resp = Response(response=json.dumps(resData), status=200, mimetype="application/json")
        return resp

    resData = {"status": 1}
    resp = Response(response=json.dumps(resData), status=200, mimetype="application/json")
    return resp

@app.route('/search/news', methods=['GET'])
def search_news():
    keyword = request.args.get('keyword', '')
    page = request.args.get('page', '')
    print keyword
    print page

    data = SearchNewsProtocol.search_news_keyword_page(keyword, page)
    if data:
        resData = {"status": 0, "data": data}
        resp = Response(response=json.dumps(resData), status=200, mimetype="application/json")
        return resp

    resData = {"status": 1}
    resp = Response(response=json.dumps(resData), status=200, mimetype="application/json")
    return resp

if __name__ == '__main__':
    app.run()