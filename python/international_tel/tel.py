from bs4 import BeautifulSoup as bs
import requests
import re
from collections import OrderedDict
import sys
from os.path import dirname, realpath
parent_dir = dirname(realpath("C:\study\snc\market_crolling\python\market_write.py"))
sys.path.append(parent_dir)
from market_write import *

class tel_code:
    def __init__(self,info):
        title,code = info
        self.title = title
        self.code = code

    def __str__(self):
        return "{}\t{}\n".format(self.title, self.code)
    
    def to_tuple(self):
        return (self.title, self.code)


def get_telCode():
    telCode_url = f"https://www.unamwiki.org/w/%EB%82%98%EB%9D%BC%EB%B3%84_%EA%B5%AD%EC%A0%9C%EC%A0%84%ED%99%94%EB%B2%88%ED%98%B8"
    res = requests.get(telCode_url)
    soup = bs(res.text, "html.parser")
    arr_telCode = soup.select("#mw-content-text > div > table:nth-child(9) > tbody > tr:nth-child(167) > td > table:nth-child(8) > tbody > tr")
    arr_tuple = []
    for telCodeTag in arr_telCode:
        try:
            code_first = telCodeTag.select("td")[0].select("a")[1]["title"].strip()
            code_last = telCodeTag.select("td")[1].text.strip().split(",")[0]
            code_last = re.sub('^[+]\s',"",code_last)
            if len(code_last) > 4 :
                continue
            code_arr = [code_first,code_last]
            arr_tuple.append(tel_code(code_arr).to_tuple())
        except:
            print("x")
    print(arr_tuple)
    file_name = "telCode"
    sheet_title = "tel"
    arr_column = ["title","code"]
    # write_excel(file_name,sheet_title, arr_column, arr_tuple)
get_telCode()