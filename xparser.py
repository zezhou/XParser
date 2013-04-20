#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re,urllib,imp,os,logging,json
from pyquery import PyQuery
from lxml.html import soupparser

class Parser:
  def __init__(self):
    self.rules = Rule()

  @classmethod
  def parse(cls,task = None, ident = None,data = None):
    if type(task) is tuple: ident,data = task
    elif type(task) is str: ident = task
    if not data and type(ident) is str: data = fetch(ident)
    handlers = parser.rules.get_handler(ident = ident)
    metadata.clear()
    for handler in handlers:
      lxmlRes=soupparser.fromstring(data)
      query = PyQuery(lxmlRes)
      handler(data,query)
    return metadata

  @classmethod
  def fetch(cls,url):
    return urllib.urlopen(url).read()

  @classmethod
  def run(cls, tasks, handle):
    for task in tasks:
      logging.debug("Handle %s" % task)
      handle(cls.parse(task))
  
  @classmethod
  def set_handler(cls,parsers = None,parser_path = None):
    if type(parsers) is not list:
      def  filter_py(f):
        if type(f) is str and len(f)>3 and f[-3:] == ".py":
          return f[0:-3]
      parsers = map(lambda f:filter_py(f),os.listdir(parser_path))
    for parser_file in parsers:
      if parser_file is not None:
        fp, pathname, description = imp.find_module(parser_file, [parser_path])
        imp.load_module(parser_file, fp, pathname, description)

  @classmethod
  def decode(cls,data):
    if type(data) == str:
      try:
        data = data.decode("utf-8")
      except:
        try:
          data = data.decode("gb2312")
        except:
          data = data.decode("gbk")
    return data

  @classmethod
  def encode(cls, data, encode_type = "utf-8"):
    if type(data) == str:
      return data
    elif type(data) == unicode:
      return data.encode(encode_type)
    elif type(data) == dict:
      encode_data = {}
      for k in data:
        encode_data[k] = cls.encode(data[k], encode_type = encode_type)
      return encode_data
    elif type(data) == list:
      encode_data = []
      for item in data:
        encode_data.push(cls.encode(item))
      return encode_data 
    else:
      logging.warning("Unsupport format data.")
      return data

class Rule:
  def __init__(self):
    self.rules = []
    self.cur_rule = {}  

  def add(self, rule, handler):
    if type(rule) is not str: raise ValueError
    rule = re.compile(rule)
    if self.cur_rule.get("handler",None):
      self.cur_rule = {"rule":rule,"handler":handler,"skips":[]}
    else:
      self.cur_rule.update({"rule":rule,"handler":handler})
    self.rules.append(self.cur_rule)

  def skip(self,pattern):
    if type(pattern) is not str: raise ValueError
    rule = re.compile(pattern)
    if self.cur_rule.get("skips"):
      self.cur_rule["skips"].append(rule)
    else:
      self.cur_rule.update({"skips":[rule]})

  def get_handler(self, ident):
    handlers = []
    for item in self.rules:
      isSkip = False
      rule = item.get('rule',None)
      handler = item.get("handler",None)
      skip_rules = item.get('skips',[])
      if type(skip_rules) is list and len(skip_rules) >0:
        for skip in skip_rules:
          if skip.match(ident):
            isSkip = True
            break
      if not isSkip and rule.match(ident):
        handlers.append(handler)
    return handlers

class Decorator:
  @classmethod
  def route(cls,pattern):
    def decorator(callback):
      parser.rules.add(pattern,callback)
      return callback
    return decorator

  @classmethod
  def skip(cls,pattern):
    def decorator(callback):
      parser.rules.skip(pattern)
      return callback
    return decorator

class Metadata(dict):
  @classmethod
  def collect(cls,name,value):
    metadata[name] = value

  def pprint(self):
    data = Parser.encode(self)
    print json.dumps(data , indent = 1, ensure_ascii = False)

parser = Parser()
metadata = Metadata()
route = Decorator.route
skip = Decorator.skip
collect = Metadata.collect
fetch = Parser.fetch
parse = Parser.parse
decode = Parser.decode
encode = Parser.encode
run = Parser.run

def main():
  """ Unit test: Get Yahoo! and Amazon's title, but skip omg.yahoo.com """
  tasks=[
    "http://www.yahoo.com",
    "http://omg.yahoo.com",
    "http://www.amazon.com"
  ]
  def handle(data):
    data.pprint()
  parser.set_handler(parser_path = "examples")
  run(tasks, handle)

if __name__=="__main__":
  main()
