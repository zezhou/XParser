#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pyquery import PyQuery as q
from lxml.html import soupparser
from xparser import route,parse,collect

@route('http://www.amazon.cn/*')
def product_page():
  collect()

if __name__=="__main__":
  result = parse()
  print result
