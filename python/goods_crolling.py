from bs4 import BeautifulSoup as bs
import requests
import re
from Kpop_artist import Kpop_artistSearch   
from goods_source import menu_resolve


def goods_crolling_start(arr_artistSearch):
    for sql_id, artistSearch in enumerate(arr_artistSearch, start=1):
        artistSearch_id = artistSearch.get_id()
        artistSearch_name = artistSearch.get_name()
    
        wevers_uri = "https://weverseshop.io"
        artist_goods=f"https://weverseshop.io/ko/shop/GL_KRW/artists/{artistSearch_id}"
        res = requests.get(artist_goods)
        soup = bs(res.text, 'html.parser')
        goods_menu = soup.select("ul.sc-3ef6c2a0-5>li")

        menu_allow_designation = re.compile(r'MERCH|ALBUM|DVD|COLLAB')

        # chat2
        # menu_resolve_mapping 정보 가져오기 
        for menu in goods_menu:
            
            menu_designation = menu.select_one("a").text.strip()

            if not menu_allow_designation.match(menu_designation):
                continue
            print(menu_designation)
            category = 'ALBUM' if menu_designation in 'ALBUM' else 'goods';
            
            menu_resolve_mapping = menu.select_one("a")["href"]
            print("{} = {}".format(category,menu_resolve_mapping))
            menu_resolve(wevers_uri, menu_resolve_mapping, sql_id, category, artistSearch_name)
        break

def read_artistSearch():
    arr_artistSearch = []
    with open("C:/snc/market_crolling/python/refer_weverse/kpop_artist.csv","r",encoding="UTF-8") as file:
        arr_artistSearch = [Kpop_artistSearch(line.strip()) for index, line in enumerate(file) if index !=0]
    goods_crolling_start(arr_artistSearch)
read_artistSearch()