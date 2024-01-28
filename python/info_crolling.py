from bs4 import BeautifulSoup as bs
from urllib.request import urlretrieve
import requests
import os
import re
from Kpop_artist import *
from kpopdb_source import *
from market_write import write_excel,write_sql
from img_down import img_down

artist_search = []
def read_artist():
    with open('C:/snc/market_crolling/python/refer_weverse/kpop_artist.csv',"r",encoding="utf-8") as file:
        artist_search = [Kpop_artistSearch(line) for i, line in enumerate(file) if i != 0]
    return artist_search 
read_artist()
artist_search = read_artist()

def kpopdb_search_start(artist_search):
    print("--------------------------------------------")
    testi=0
    arr_artist_info = []
    for index, artist_name in enumerate(artist_search, start=1):


        lower_name = artist_name.get_lower_name()
        part_group = artist_name.get_group()
        url=f"https://dbkpop.com/{part_group}/{lower_name}/"

        print("---------------------------\n")

        print(lower_name)
        
        print("---------------------------\n")

        res = requests.get(url)
        soup = bs(res.text, 'html.parser')
        #name
        main_name =artist_name.get_name()
        #korean name
        # div#field_5813754fe09f2
        try:
            sub_name = soup.select_one("#field_58138011b1cf6").text.strip()
        except:
            sub_name = soup.select_one("#field_5813754fe09f2").text.strip()

        #  debut
        artist_debut = artist_debut_output(soup)

        print("{} {} {}".format(main_name,sub_name,artist_debut))

        # Todo member_info
        member_toJson = member_output(soup)
        print("member_toJson = {}".format(member_toJson))

        # Todo sns
        sns_tojson =sns_output(soup)
        print("sns_tojson = {}".format(sns_tojson))
                    
        # Todo mv
        mv_toJson = mv_output(soup)
        print("mv_toJson = {}".format(mv_toJson))

        # TODO img
        img_toJson=img_output(soup)
        print("img_toJson = {}".format(img_toJson))
        
        # img url download
        json_object = json.loads(img_toJson)
        arr_img_url = json_object["img"]
        arr_dirPath = [f'C:/snc/market_crolling/img/artist\info/{main_name}']
        down_image_json = img_down(arr_img_url, arr_dirPath)
        print("down_image_json = {}".format(down_image_json))

        arr_artist_source = [main_name, 
                            sub_name, 
                            artist_debut, 
                            sns_tojson,
                            member_toJson, 
                            mv_toJson, 
                            down_image_json] 
        arr_artist_info.append(arr_artist_source)
    # sql
    arr_artist_info=[Kpop_artistSql(i) for i in arr_artist_info]
    
    print("SQL start!!!")

    file_name = "artist"
    sheet_title = "info"
    arr_cloumn = ["id","name","korean_name", "debut", "sns","member","mv","artist_img"]
    write_excel(file_name, sheet_title, arr_cloumn, arr_artist_info)
    insert_sql = "insert into Artist(name, korean_name, debut, sns, member, mv, artist_img) values(%s, %s, %s, %s, %s, %s, %s)"
    for k_artistsql in arr_artist_info:
        tuple_data = k_artistsql.to_tuple()
        write_sql(tuple_data, insert_sql)
    
    print("sql compleate!!!!!")
    print("--------------------------------------------")

kpopdb_search_start(artist_search)
