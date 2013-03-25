#!/usr/bin/env python
# -*- coding: utf-8 -*-
from xparser import run,parse,skip

@parse('http://www.amazon.cn/*')
@skip('http://www.amazon.cn/help')
def product_page():
  pass


tasks = [
  'http://www.amazon.cn/1' ,
  ('test.com',"<html>hello world</html>")
]

if __name__=="__main__":
  run(tasks = tasks)
