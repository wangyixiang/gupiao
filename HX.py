# -*- coding: utf-8 -*-

import json
import logging
import pyquery
import re
import urllib2
import const
import StringIO

from stockbase import StockDataCrawler
from helper import get_sha_stock_list, get_sza_stock_list



class StockDataCrawlerOnHX(StockDataCrawler):
    base_url = r"http://stockdata.stock.hexun.com/"
    #%s part fill with stock number
    stockholders_url = "2009_cgjzd_%s.shtml"
    def __init__(self, number, name):
        super(StockDataCrawlerOnHX,self).__init__(number, name)
        self.opener = urllib2.build_opener()
        self.opener.addheaders = [("User-agent", "Mozilla/5.0")]
    
    def get_holder_statistic_from_web(self):
        """
        it will return a dict which include data in following format:
        {
        "year-month-day": {"th":totalholders,"ph":perholdings,"phcr":perholdingchangeratio,"ts":totalshares,"trs": tradableshares}
        }
        """
        q1p = re.compile(u"(?P<year>\d+)" + const.NIAN + const.DI + u"(?P<quarter>\d+)" + const.JI)
        q2p = re.compile(u"(?P<year>\d+)" + const.NIAN + const.ZHONGQI)
        q3p = re.compile(u"(?P<year>\d+)" + const.NIAN + const.QIAN + u"(?P<quarter>\d+)" + const.JI)
        q4p = re.compile(u"(?P<year>\d+)" + const.NIAN + const.NIAN + const.DU)

        records = self._get_holder_statistics_webdata()
        if self.holder_statistic == None :
            self.holder_statistic = {}
        for r in records:
            tdq = pyquery.PyQuery(r)
            tds = tdq("td span")
            ymd = ""
            m1 = q1p.search(tds[0].text)
            m2 = q2p.search(tds[0].text)
            m3 = q3p.search(tds[0].text)
            m4 = q4p.search(tds[0].text)
            if m1:
                ymd = u"20%s-03-31" % m1.group("year")
            elif m2:
                ymd = u"20%s-06-30" % m2.group("year")
            elif m3:
                ymd = u"20%s-09-30" % m3.group("year")
            elif m4:
                ymd = u"20%s-12-31" % m4.group("year")
            else:
                logging.warn(u"malformed data on %06d \n data:%s" % (self.number, tds[0]))
                
            self.holder_statistic[ymd] = {
                "th" : tds[1].text,
                "ph" : tds[2].text,
                "phcr" : tds[3].text,
                "ts" : tds[4].text,
                "trs" : tds[5].text
            }
    
    def _get_holder_statistics_webdata(self):
        target_url = ''.join([self.base_url, self.stockholders_url % self.number])
        logging.info("Open data url at %s ." % target_url)
        f = self.opener.open(target_url)
        logging.info("Reading data.")
        d = f.read()
        f.close()
        if d == "":
            logging.warn("No data after reading operation completed.")
        else:
            logging.info("Done.")
            
        d = pyquery.PyQuery(d)
        p = d("div#zaiyaocontent table.web2 tr")
        return p[2:-1]
    
    def _write_holder_statistic_as_json(self):
        jsondata = StringIO.StringIO()
        if self.holder_statistic:
            keys = self.holder_statistic.keys()
            keys.sort()
            jsondata.write(json.dumps(self.holder_statistic))
            #for key in keys:
                #jsondata.write(json.dumps(self.holder_statistic[key]))
                #jsondata.write("\n")
        return jsondata.getvalue()
    
if __name__ == "__main__":
    sha = get_sha_stock_list()
    sza = get_sza_stock_list()
    #for key in sza.keys():
        #sdc = StockDataCrawlerOnHX(key,sza[key])
        #try:
            #p = sdc.get_holder_statistic_from_web()
            #afile = file(r"jsonraw\%s.json" % key, "w+")
            #afile.write(sdc._write_holder_statistic_as_json())
            #afile.close()
        #except Exception, e:
            #logging.exception(key)
    key = "600000"
    sdc = StockDataCrawlerOnHX(key,sha[key])
    p = sdc.get_holder_statistic_from_web()
    afile = file(r"jsonraw\%s.json" % key, "w+")
    afile.write(sdc._write_holder_statistic_as_json())
    afile.close()