#!/usr/bin/env python
# -*- coding: utf-8 -*-
from xparser import route,collect,skip

@route("http://*.yahoo.com/*")
@skip("http://omg.yahoo.com/*")
def get_title(data,query):
    title = query("title").text()
    collect("title",title)
