#!/usr/bin/env python
# -*- coding: utf-8 -*-
from xparser import route,collect

@route("http://*.amazon.com/*")
def get_title(data,query):
    title = query("title").text()
    collect("title",title)
