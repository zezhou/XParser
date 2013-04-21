#!/usr/bin/env python
# -*- coding: utf-8 -*-
try:
    from xparser import route,collect,skip
except:
    import sys
    sys.path.insert(0, "../")
    from xparser import route,collect,skip
@route("http://.*\.yahoo\.com.*")
@skip("http://omg.yahoo.com/*")
def get_title(data,query):
    title = query("title").text()
    collect("title",title)

if __name__=="__main__":
    from xparser import parse
    print parse("http://www.yahoo.com")
