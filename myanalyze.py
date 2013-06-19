# -*- coding: utf-8 -*-

import json
import os

from helper import get_sha_stock_list, get_sza_stock_list

sha = get_sha_stock_list()
sza = get_sza_stock_list()

sha_keys = sha.keys()
sha_keys.sort()
sza_keys = sza.keys()
sza_keys.sort()

window = ("2013-03-31", "2012-12-31", "2012-09-30")
sha_hs = sza_hs = {}
dpp = r"json" + os.sep + r"%s.json"

for key in sha_keys:
    fp = open(dpp % key)
    sha_hs[key] = json.load(fp)
    fp.close()
    
for key in sza_keys:
    fp = open(dpp % key)
    sza_hs[key] = json.load(fp)
    fp.close()
    
sha_w = {}
for w in window:
    sha_w[w] ={}
    for key in sha_keys:
        try:
            sha_w[w][sha_hs[key][w]["minv"]].append(key)
        except KeyError:
            try:
                sha_w[w][sha_hs[key][w]["minv"]] = [key]
            except KeyError:
                print key

sza_w = {}

for w in window:
    sza_w[w] = {}
    for key in sza_keys:
        try:
            sza_w[w][sza_hs[key][w]["minv"]].append(key)
        except KeyError:
            try:
                sza_w[w][sza_hs[key][w]["minv"]] = [key]
            except KeyError:
                print key
import pprint

pprint.pprint(sha_w)
pprint.pprint(sza_w)