#!/usr/bin/env python
# -*- coding: utf-8 -*-
try:
    from xparser import route,collect
except:
    import sys
    sys.path.insert(0, "../")
    from xparser import route,collect

@route("http://.*\.amazon\.com")
def get_title(data,query):
    print data, "get title"
    title = query("title").text()
    collect("title",title)

if __name__=="__main__":
    from xparser import parse
    print parse("http://www.amazon.com")

