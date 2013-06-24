# -*- coding: utf-8 -*-

import logging
import os

import stockbase
import const

def get_stocks_from_rbb(datafile):
    pass

def get_stocks_from_qjfxbb(datafile):
    """
    return a dict which contain stock base info from qjfxbb
    """
    txt_ext = ".txt"
    xls_ext = ".xls"
    ext = os.path.splitext(datafile)[1]
    resultdict = {}
    if not os.path.exists(datafile):
        return resultdict
    dfile = open(datafile)
    datalines = dfile.readlines()
    dfile.close()
    dataposdict = {
        'number': -1,
        'name': 0,
        'er' : 0,
        'cr' : 0,
        'range': 0,
        'volume': 0,
        'turnover':0,
        'price': -1
    }
    dataposmark = {
        u"代码":"number",
        u"名称":"name",
        u"换手率":"er",
        u"涨跌幅度":"cr",
        u"振荡幅度":"range",
        u"成交量":"volume",
        u"总金额":"turnover",
        u"收盘": "price"
    }
    datamarklist = unicode(datalines[1],"utf-8").split()
    dpmkeys = dataposmark.keys()
    for dpmkey in dpmkeys:
        i = 0
        while i < len(datamarklist):
            if datamarklist[i].strip("%") == dpmkey:
                dataposdict[dataposmark[dpmkey]] = i
                break
            i += 1
    
    for dataline in datalines:
        dataline = unicode(dataline, "utf-8")
        datas = dataline.split(u"\t")
        if ext.lower() == xls_ext:
            #xls row format and meaning
            #
            if dataline[:2] != '="':
                continue
            datas[0] = datas[0].strip('="')
        else:
            if not dataline[:2].isdigit():
                continue
            
        if len(datas) < 13:
            print str(datas[0])
            continue        
        
        onestock = resultdict[datas[dataposdict["number"]].strip()] = stockbase.StockBase(
            datas[dataposdict["name"]].strip(),
            datas[dataposdict["number"]].strip()
        )
        
        onestock.exchange_rate = datas[dataposdict["er"]].strip()
        if onestock.exchange_rate:
            onestock.exchange_rate = float(onestock.exchange_rate)
        onestock.change_rate = datas[dataposdict["cr"]].strip()
        if onestock.change_rate:
            onestock.change_range = float(onestock.change_rate)
        onestock.volume = datas[dataposdict["volume"]].strip()
        if onestock.volume:
            if onestock.volume[-1] == const.YI:
                onestock.volume = int(float(onestock.volume[:-1]) * (10 ** 8))
            elif onestock.volume[-1] == const.WAN:
                onestock.volume = int(float(onestock.volume[:-1]) * (10 ** 4))
            elif onestock.volume[-1].isdigit():
                onestock.volume =int(onestock.volume)
            else:
                logging.warn("May have problem on parsing stock %s volume" % onestock.number)  
        onestock.turnover = datas[dataposdict["turnover"]].strip()
        if onestock.turnover:
            if onestock.turnover[-1] == const.YI:
                onestock.turnover = int(float(onestock.turnover[:-1]) * (10 ** 8))
            elif onestock.turnover[-1] == const.WAN:
                onestock.turnover = int(float(onestock.turnover[:-1]) * (10 ** 4))
            elif onestock.turnover[-1].isdigit():
                onestock.turnover =int(onestock.turnover)
            else:
                logging.warn("May have problem on parsing stock %s volume" % onestock.number)         
        onestock.change_range = datas[dataposdict["range"]].strip()
        if onestock.change_rate:
            onestock.change_rate = float(onestock.change_rate)
        onestock.price = datas[dataposdict["price"]].strip()
        if onestock.price:
            onestock.price = float(onestock.price)
        
    return resultdict

def test_get_stocks_from_qjfxbb():
    import StringIO
    import os
    stocks = get_stocks_from_qjfxbb(ur"d:\work\gupiao\tdx\报表分析.TXT")
    keys = stocks.keys()
    keys.sort()
    sb = StringIO.StringIO()
    sb.write(os.linesep)
    for key in keys:
        astock = stocks[key]
        if not (astock.price and astock.exchange_rate and astock.change_rate):
            print str(key)
            continue
        if ((astock.price < 15.0) and
            (astock.exchange_rate < 4.0) and
            (astock.change_rate > -2.0)
            ):
            if key[0] == u"6":
                sb.write(u"1" + key + os.linesep)
            else:
                sb.write(u"0" + key + os.linesep)
    #afile = open(ur"d:\work\gupiao\a.ebk", "w+")
    #afile.write(sb.getvalue())
    #afile.close()
    keys = sb.getvalue().split(os.linesep)
    hs_stock = {}
    for key in keys:
        if not key.strip() or key[1] == u"3":
            continue
        sa = stockbase.StockAnalyzing(key[1:],"")
        sa._get_holder_statistic_from_json(ur"json\%s.json" % key[1:])
        try:
            hs_stock[sa.holder_statistic["2013-03-31"]["minv"]].append(key)
        except KeyError:
            try:
                hs_stock[sa.holder_statistic["2013-03-31"]["minv"]] = [key]
            except KeyError:
                print key
    
    import pprint
    pprint.pprint(hs_stock)
    
if __name__ == "__main__":
    pass