# -*- coding: utf-8 -*-

import StringIO
import logging

from const import KIND_MARKET_SHANGHAI_A_SHARE, KIND_MARKET_SHENGZHEN_A_SHARE
from const import SHSML, SZSML

def get_sha_stock_list():
    return _get_stock_list(KIND_MARKET_SHANGHAI_A_SHARE)

def get_sza_stock_list():
    return _get_stock_list(KIND_MARKET_SHENGZHEN_A_SHARE)

def _get_stock_list(kind):
    """
    return a dict which using number as key and name as value;
    """
    rawdata = None
    result = {}
    numformat = "%06d"
    if kind == KIND_MARKET_SHANGHAI_A_SHARE:
        rawdata = SHSML
    elif kind == KIND_MARKET_SHENGZHEN_A_SHARE:
        rawdata = SZSML
        
    if rawdata == None:
        return result
    
    data = StringIO.StringIO(rawdata)
    datalines = data.readlines()
    data.close()
    for i in range(2, len(datalines)):
        dataline = datalines[i].split()
        result[numformat % int(dataline[0].strip())] = dataline[1].strip()
        
    return result