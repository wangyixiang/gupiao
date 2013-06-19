# -*- coding: utf-8 -*-
import urllib2
fullurl = r"http://stockdata.stock.hexun.com/2009_cgjzd_600867.shtml"
#f = urllib2.urlopen("http://stockdata.stock.hexun.com/2009_cgjzd_600867.shtml")
opener = urllib2.build_opener()
opener.addheaders = [("User-agent","Mozilla/5.0")]
f = opener.open(fullurl)
data = f.read()
print data