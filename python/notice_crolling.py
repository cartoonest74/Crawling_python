from bs4 import BeautifulSoup as bs
import requests
import re
import json
from collections import OrderedDict
from Kpop_artist import Kpop_artist
from Kpop_artist import Kpop_artistSearch  
from Kpop_artist import Artist_notice  
from market_write import write_sql, write_excel
from img_down import img_down
# base64 decode
import base64
import io
from PIL import Image

def to_json(key_title,arr_val):
    odict = OrderedDict()
    odict[key_title] = arr_val
    list_to_json = json.dumps(odict,indent= 4, ensure_ascii = False)
    return list_to_json

def notice_crolling_start(arr_artistSearch):
    for sql_id, artistSearch in enumerate(arr_artistSearch, start=1):
        notice_page = 1
        artist_id = artistSearch.get_id()
        artist_name = artistSearch.get_name()

        while notice_page <= 6:  
            artist_notice = f"https://weverseshop.io/ko/shop/GL_KRW/artists/{artist_id}/notices?page={notice_page}"
            notice_page = notice_page + 1
            res = requests.get(artist_notice)
            soup = bs(res.text, "html.parser")
            notice_menu = soup.select("li.sc-ed114d78-2")
            if len(notice_menu) == 0:
                break
            first_notice_menu(sql_id, notice_menu, artist_name)

def first_notice_menu(sql_id, notice_menu, artist_name):
    arr_notice_subTitleBox =[]

    for menu in notice_menu:
        notice_link = menu.select_one("a.sc-ed114d78-3")["href"]
        arr_notice_subTitleBox = menu.select("div.sc-aff297c7-6")
        arr_notice_subTitle =[]
        for notice_subTitle in arr_notice_subTitleBox:

            notice_content_list = OrderedDict()
            arr_notice_subTitle=notice_subTitle.select("li.sc-aff297c7-1")
            # 공통 부분 제외
            if len(arr_notice_subTitle) < 2:
                continue

            notice_title = notice_subTitle.select_one("p.sc-aff297c7-2").text.strip()
            title_list_to_json = to_json("title",notice_title)
            notice_date = notice_subTitle.select_one("time")['datetime']
            notice_category = arr_notice_subTitle[0].text.strip()


            # content
            wevers_notice_uri = f"https://weverseshop.io{notice_link}"
            notice_res = requests.get(wevers_notice_uri)
            notice_soup = bs(notice_res.text, "html.parser")
            arr_notice_content = notice_soup.select("div.sc-96157d9a-3>p")
            notice_content = '\n'.join(str(item) for item in arr_notice_content)
            
            # print(notice_content)
            image_dataUrl_reg = re.compile('^(data:)')
            arr_img_data = notice_soup.find_all(src=image_dataUrl_reg)
            arr_dirPath=[f'C:/study/snc/market_crolling/img/artist/notice/{artist_name}']
            
            arr_imgData_src =[]
            if len(arr_img_data) > 0 :
                arr_imgData_src=[img_data_tag["src"] for img_data_tag in arr_img_data]
                down_iamge_json = img_down(arr_imgData_src, arr_dirPath)
                for index, img_data_tag in enumerate(arr_img_data):
                    img_data_src=img_data_tag["src"]
                    down_image_url = json.loads(down_iamge_json)['img'][index][0]
                    notice_content = notice_content.replace(img_data_src,down_image_url)
                    
            content_list_to_json = to_json("content", f'{notice_content}')

            # 정리
            arr_notice_source = [sql_id,
                                notice_category,
                                title_list_to_json,
                                content_list_to_json,
                                notice_date]
            sql = "insert into artist_notice(artist_id, category, title, content, date) values(%s, %s, %s, %s, %s)"
            tuple_data=Artist_notice(arr_notice_source).to_tuple()
            # print(tuple_data)
            write_sql(tuple_data,sql)


def read_artistSearch():
    arr_artistSearch = []
    with open("C:/study/snc/market_crolling/python/refer_weverse/kpop_artist.csv","r",encoding="UTF-8") as file:
        arr_artistSearch = [Kpop_artistSearch(line.strip()) for index, line in enumerate(file) if index !=0]
    notice_crolling_start(arr_artistSearch)
read_artistSearch() 