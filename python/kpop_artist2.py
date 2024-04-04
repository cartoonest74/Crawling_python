from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs
from urllib.request import urlretrieve
import requests
import os
import re
from Kpop_artist import *
from market_write import write_excel, write_sql
from img_down import img_down, group_img_down
from kpopdb_source2 import *

artist_search = []


def read_artist():
    with open(
        "C:/snc/market_crolling/python/refer_weverse/kpop_artist.csv",
        "r",
        encoding="utf-8",
    ) as file:
        artist_search = [
            Kpop_artistSearch(line) for i, line in enumerate(file) if i != 0
        ]
    return artist_search


read_artist()
artist_search = read_artist()


def get_kpopdb_sns(artist_search):
    href_reg = re.compile('(href=.*"){1}')
    class_reg = re.compile('class[=](["].*["])')
    arr_sns_info = []
    arr_sns_column = []
    for index, artist_name in enumerate(artist_search, start=1):
        sql_id = index
        lower_name = artist_name.get_lower_name()
        part_group = artist_name.get_group()

        url = f"https://kpopping.com/profiles/{part_group}/{lower_name}"

        print("---------------------------\n")

        print(lower_name)

        print("---------------------------\n")

        res = requests.get(url)
        soup = bs(res.text, "html.parser")
        socials = soup.select("div.socials")
        arr_socials = socials[0].select("a")
        sns_orderDict = OrderedDict()
        sns_orderDictBox = OrderedDict()
        list_to_json = ""
        for social in arr_socials:
            social_href = href_reg.search(f"{social}").group().split('"')[1].strip()

            social_class = class_reg.search(f"{social}").group()
            arr_socials_title = social_class.strip().split("-")
            social_title = arr_socials_title[1].split('"')[0].strip()

            print("social_href={}".format(social_href))
            print("social_title={}".format(social_title))
            sns_orderDict[social_title] = social_href
            list_to_json = json.dumps(sns_orderDict, indent=4, ensure_ascii=False)
        arr_sns_source = [sql_id, lower_name, list_to_json]
        arr_sns_info.append(arr_sns_source)
    arr_sns_info = [sns(val) for val in arr_sns_info]
    file_name = "sns"
    sheet_title = "sns"
    arr_sns_column = [
        "id",
        "lower_name",
        "sns",
    ]
    write_excel(file_name, sheet_title, arr_sns_column, arr_sns_info)


# get_kpopdb_sns(artist_search)


def kpopdb_search_start(artist_search):
    print("---------------------------------------")
    arr_artist_info = []
    sql_id = 0
    for index, artist_name in enumerate(artist_search, start=1):
        sql_id = index
        lower_name = artist_name.get_lower_name()
        part_group = artist_name.get_group()

        url = f"https://kpopping.com/profiles/{part_group}/{lower_name}"

        print("---------------------------\n")

        print(lower_name)

        print("---------------------------\n")

        res = requests.get(url)
        soup = bs(res.text, "html.parser")

        # member img
        main_name = artist_name.get_name()
        # memberImg_json = group_MemberImg(soup, main_name, part_group)

        # discography
        # discography_json = get_album(soup, main_name, url)

        # main Img
        mainImg_json = get_mainImg(soup, main_name)
        arr_artist_source = []
        arr_artist_source = [sql_id, main_name, mainImg_json]
        arr_artist_info.append(arr_artist_source)
    arr_artist_info = [mainImg(val) for val in arr_artist_info]

    file_name = "mainImg_href"
    sheet_title = "info"
    arr_column = ["id", "artist", "mainImg"]
    write_excel(file_name, sheet_title, arr_column, arr_artist_info)


kpopdb_search_start(artist_search)
