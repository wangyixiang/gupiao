# -*- coding: utf-8 -*-

import json

class StockDataCrawler(object):
    def __init__(self, number, name):
        self.name = name
        self.number = number
        self.holder_statistic = None
        
    def get_holder_statistic(self):
        raise NotImplementedError()
        
class StockBase(object):
    P_DAY = u"day"
    P_WEEK = u"week"
    P_MONTH = u"month"
    P_YEAR = u"year"
    
    def __init__(self, name=None, number=None, period=P_DAY):
        self.name = name
        self.number = number
        self.period = period
        self.period_number = 1
        self.exchange_rate = -1
        self.change_rate = 0
        self.volume = -1
        self.turnover = -1
        self.total_share = -1
        self.tradable_share = -1
        self.change_range = -1
        self.price = -1
        self.total_holder = -1
        self.perholding = -1
        self.industry_sector = None
        self.listing_date = None
    

class StockAnalyzing(object):
    def __init__(self, number, name):
        self.number = number
        self.name = name
        self.holder_statistic = None
        
    def _get_holder_statistic_from_json(self, json_data_file):
        jdf = open(json_data_file)
        self.holder_statistic = json.load(jdf)
        
    def holder_statistic_th_values(self, bits=7):
        if bits < 3:
            pass
        keys = self.holder_statistic.keys()
        keys.sort(reverse=True)
        klen = len(keys)
        minv = bits * (10**(bits+1))
        if klen <= 4:
            for key in keys:
                self.holder_statistic[key]["minv"] = minv
            return
        starti = 0
        endi = klen - 4
        for ii in range (-4, 0):
            self.holder_statistic[keys[ii]]["minv"] = minv
        while starti < endi:
            tminv = minv
            for i in range(1, bits+1):
                try:
                    if float(self.holder_statistic[keys[starti]]["th"].replace(u",","")) <= \
                    float(self.holder_statistic[keys[starti + i]]["th"].replace(u",","")):
                        tminv += 10 ** (bits + 1 - i)
                except IndexError:
                    pass
            self.holder_statistic[keys[starti]]["minv"] = tminv
            starti += 1
            
    
def holder_statistic_th_values():
    import helper
    import json
    sha = helper.get_sha_stock_list()
    sza = helper.get_sza_stock_list()
    sha_keys = sha.keys()
    sha_keys.sort()
    sza_keys = sza.keys()
    sza_keys.sort()
    sha_hs = {}
    sza_hs = {}
    for key in sha_keys:
        sa = StockAnalyzing(key, sha[key])
        hs = sa._get_holder_statistic_from_json(r'json\%s.json' % key)
        sa.holder_statistic_th_values()
        sha_hs[key] = sa.holder_statistic
        afile = file(r"json\%s.json" % key, "w+")
        json.dump(sa.holder_statistic, afile)
        afile.close()
        
    for key in sza_keys:
        sa = StockAnalyzing(key, sza[key])
        hs = sa._get_holder_statistic_from_json(r'json\%s.json' % key)
        sa.holder_statistic_th_values()
        sza_hs[key] = sa.holder_statistic
        afile = file(r"json\%s.json" % key, "w+")
        json.dump(sa.holder_statistic, afile)
        afile.close()        
        
if __name__ == "__main__":
    pass