from collections import OrderedDict
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup as bs
import re

image_url_reg = re.compile('url\(["].*["]')
def to_json(key_title,arr_val):
    odict = OrderedDict()
    odict[key_title] = arr_val
    list_to_json = json.dumps(odict,indent= 4, ensure_ascii = False)
    return list_to_json

#  조건식으로 숨겨져있는 option 부분 selenium으로 가져오기
def option_click(more_goods_option,more_goods_url):
    key_title="option"

    if more_goods_option is None:
        po_list_to_json = to_json(key_title,'')
        return po_list_to_json

    browser = webdriver.Chrome()
    browser.get(more_goods_url)
    browser.maximize_window()
    time.sleep(2)
    browser.execute_script("window.scrollTo(0, 0)") 
    element = browser.find_element(By.CLASS_NAME,"weverse-select__control")
    element.click()
    option_html = browser.page_source
    time.sleep(2)
    option_soup = bs(option_html, 'html.parser')
    option_list = []
    option_list = option_soup.select('div.css-b62m3t-container>div[class="weverse-select__menu css-1nmdiq5-menu"]>div')
    option_list = option_list[0].select('div[aria-disabled="false"]')
    
    arr_option = []
    for size in option_list:
        size_designation = size.select_one('div.sc-bb1f6358-2').text.strip()
        arr_option.append([size_designation,50])

    po_list_to_json = to_json(key_title,arr_option)
    print('po_list_to_json =  {}'.format(po_list_to_json))
    return po_list_to_json

# 상품설명 부분 이미지
def product_description(more_goods_soup):
    more_goods_body = more_goods_soup.select('section.sc-61581632-16>section>div>div>span') 
    arr_pdi = []
    for more_goods in more_goods_body:
        goods_body_src = more_goods.select_one('img[data-nimg="intrinsic"]')["style"]
        goods_body_src = image_url_reg.search(goods_body_src).group().split('"')[1]
        arr_pdi.append(goods_body_src)
    
    return arr_pdi

# 상품공지 부분
def product_notice_part(more_goods_soup):
    key_title="p_notice"
    more_goods_notice = more_goods_soup.select('dl.sc-86dc95fe-0>div')
    arr_pn = []
    for notice_product in more_goods_notice:  
        dt= notice_product.find("dt").text.strip()
        dd= notice_product.find("dd").text.strip()
        arr_pn.append([dt,dd])
    # json 변환시 한글 깨짐

    # ensure_ascii = False 방지
    # OrderedDict => json 변환
    pn_list_to_json = to_json(key_title, arr_pn)
    print('pn_list_to_json = {}'.format(pn_list_to_json))
    return pn_list_to_json