from bs4 import BeautifulSoup as bs
import requests
import re
from collections import OrderedDict
from Kpop_artist import Kpop_artist
from more_good_page_source import *  
from Artist_product import Artist_product
from market_write import write_sql, write_excel
from img_down import img_down

# chat 1
# cite artist id 가져오기
def get_cite_artist_id():
    artist_id_url=f"https://weverseshop.io/ko/home"
    res = requests.get(artist_id_url)
    soup = bs(res.text, 'html.parser')

    artist_ul = soup.select("ul[class='sc-2e490289-15 fmWxil']>li")

    artist_list = OrderedDict()
    for info in artist_ul:
        artist_id = info.select_one('nav[class="sc-93ef7887-4 eFQQDo"]>a')["data-artist-id"]
        artist_name = info.select_one('h4[class="sc-93ef7887-3 jexiQo"]').text.strip()
        artist = Kpop_artist(artist_id, artist_name)
        artist.set_kpop_list()
        artist_list = artist.get_kpop_list()
    return artist_list

# chat 1 정보 기록하기
def write_artist_id(artist_list):
    with open('./python/refer_weverse/re_kpop_artist.csv','w',encoding='UTF-8') as file:
        file.write("Id\tName\tlower_name\tgroup\n")
        for key, val in  artist_list.items():
            lower_name = val.lower()
            file.write("{}\t{}\t{}\tgroup\n".format(key,val,lower_name))


def write_artist_product(artist_list):
    with open('kpop_artist_product.csv','w',encoding='UTF-8') as file:
        file.write("artist_id\tcategory\tname\tprice\toption_size\toption_ment\tnotice\n")
        for key, val in  artist_list.items():
            file.write("{}\t{}\n".format(key,val))

#chat3
def more_goods_page(more_goods_url, sql_id, category, artistSearch_name):
    image_url_reg = re.compile('url\(["].*["]')

    more_goods_res = requests.get(more_goods_url)
    more_goods_soup = bs(more_goods_res.text,'html.parser')
    more_goods_head = more_goods_soup.select('div.sc-61581632-3>div')

    #상품 옵션부분
    more_goods_option = more_goods_soup.select_one('div.weverse-select__control')
    option_list_to_json = option_click(more_goods_option, more_goods_url)
    print(f"option_list_to_json = {option_list_to_json}")

    #상품타이틀
    more_goods_Title = more_goods_head[1].find("h2").text.strip()

    #상품 상단 메인이미지
    arr_MainImage = []
    more_goods_MainImage = more_goods_head[0].find("img")["style"]
    more_goods_MainImage = image_url_reg.search(more_goods_MainImage).group().split('"')[1]
    arr_MainImage.append(more_goods_MainImage)   
    #상품 가격 
    price = more_goods_head[1].find("strong").text.strip()
    
    # 옵션 제한 멘트
    try:
        option_limit_comment = more_goods_head[1].select_one("div.sc-eabdcbcb-14>div>div>p").text.strip()
    except:
        option_limit_comment = ''
    print(f"{more_goods_Title} = {more_goods_MainImage}\n{price}\t{option_limit_comment}\n")

    # 상품설명 부분 이미지
    arr_pdi = product_description(more_goods_soup)
    # 상품공지 부분
    pn_list_to_json = product_notice_part(more_goods_soup)
    
    # img_down
    arr_dirPath = [f'C:/snc/market_crolling/img/artist/product/{artistSearch_name}',
                    f'C:/snc/market_crolling/img/artist/product/{artistSearch_name}/{category}']

    down_main_iamge_json = img_down(arr_MainImage, arr_dirPath)
    down_sub_iamge_json = img_down(arr_pdi, arr_dirPath)

    # 정리
    arr_goods_source = [sql_id,
                        more_goods_Title,
                        category,
                        price,
                        option_list_to_json,
                        option_limit_comment,
                        pn_list_to_json,
                        down_main_iamge_json,
                        down_sub_iamge_json]
    
    artist_product  = Artist_product(arr_goods_source)
    #  sql save
    tuple_data = artist_product.to_tuple()
    sql = "insert into Product_artist(artist_id, title, category, price, option_size, option_ment, notice, main_img, sub_img) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    write_sql(tuple_data,sql)



#chat2에서 가져온 정보를 바탕으로 수행
# menu_resolve 
def menu_resolve(wevers_uri, menu_resolve_mapping, sql_id, category, artistSearch_name, next_page_count=1):
    menu_full_url = f'{wevers_uri}{menu_resolve_mapping}?page={next_page_count}'
    menu_full_res = requests.get(menu_full_url)
    menu_full_soup = bs(menu_full_res.text, 'html.parser')
    goods_list = menu_full_soup.select('ul.sc-ee91b503-1>li[data-inview="true"]')
    page_len = len(menu_full_soup.select('ol.sc-595593d8-1>li'))
    
    # 다음페이지 카운터
    next_page_count += 1
    # print('page_count = {}'.format(next_page_count))
    for goods in goods_list:
        # 품절 체크
        try:
            sale_discontinued_check = goods.find('strong',"sc-19044b37-1").text.strip()
        except:
            sale_discontinued_check = ''

        if len(sale_discontinued_check) != 0:
            continue
    
        # goods 상품명 & 상품상세페이지로 가는 주소 가져오기
        # goods_title = goods.select_one('a')["title"]
        goods_resolve = goods.select_one('a')["href"]
    
        more_goods_url =f'{wevers_uri}{goods_resolve}' 
        
        more_goods_page(more_goods_url, sql_id, category, artistSearch_name)

    if next_page_count <= page_len:
        return menu_resolve(wevers_uri, menu_resolve_mapping, sql_id, category, artistSearch_name, next_page_count)