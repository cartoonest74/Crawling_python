from bs4 import BeautifulSoup as bs
from selenium.webdriver.common.by import By
import requests
from collections import OrderedDict
from selenium import webdriver
import time
import json
from img_down import img_down, group_img_down, album_img_down


def get_mainImg(soup, main_name):
    arr_dirPath = []
    arr_memberImg = []
    mainImg_box = soup.select("div.box.encyclopedia")
    mainImg_src = mainImg_box[0].select_one("figure>div")["data-bg"]
    mainImg_ImgSrc = f"https://kpopping.com{mainImg_src}"
    mainImg_dirPath = f"C:/snc/market_crolling/img/artist/info/{main_name}/main"
    arr_memberImg.append(mainImg_ImgSrc)
    arr_dirPath.append(mainImg_dirPath)
    down_image_json = group_img_down(arr_memberImg, arr_dirPath)
    return down_image_json


def group_MemberImg(soup, main_name, part_group):
    arr_dirPath = []
    arr_memberImg = []
    if "group" in part_group:
        select_member = "div.summary.summary-only-one"
        member_list = soup.select(select_member)
        for member in member_list:
            member_ImgSrc = member.select_one("figure>a")["data-bg"]
            member_name = member.select_one("figure>a")["title"].strip().upper()

            member_ImgSrc = f"https://kpopping.com{member_ImgSrc}"
            member_dirPath = (
                f"C:/snc/market_crolling/img/artist/info/{main_name}/{member_name}"
            )

            arr_memberImg.append(member_ImgSrc)
            arr_dirPath.append(member_dirPath)
    down_image_json = group_img_down(arr_memberImg, arr_dirPath)
    return down_image_json


def get_album(soup, main_name, url):
    album_OrderDict = OrderedDict()
    albumInfo_OrderDict = OrderedDict()
    discography_soup = ""

    browser = webdriver.Chrome()
    browser.get(url)
    browser.maximize_window()

    arr_albums = []
    while True:
        try:
            time.sleep(2)
            element = browser.find_element(
                By.XPATH, "/html/body/div[3]/div/div[1]/div[7]/div/button"
            )
            if element is None:
                break
            browser.execute_script("arguments[0].click();", element)
            time.sleep(2)
            discography_html = browser.page_source
            discography_soup = bs(discography_html, "html.parser")
            arr_albums = discography_soup.select('a.item[aria-label="album"]')
        except:
            print("except!!!")
            browser.close()
            break
    for index, discography in enumerate(arr_albums):
        json_key = f"img{index}"
        album_href = discography["href"]
        album_name = discography.select_one("img")["alt"].strip()
        album_src = discography.select_one("img")["src"].strip()
        album_date = discography.select_one("time")["datetime"].strip()
        album_trackLength = discography.select_one("p").string

        album_src = f"https://kpopping.com{album_src}"
        album_dirPath = f"C:/snc/market_crolling/img/artist/info/{main_name}/album"
        arr_dirPath = []
        arr_dirPath.append(album_dirPath)
        down_image_path = album_img_down(album_src, arr_dirPath)

        print("album_href={}".format(album_href))
        # get album track
        album_path = f"https://kpopping.com{album_href}"
        album_res = requests.get(album_path)
        album_soup = bs(album_res.text, "html.parser")

        album_tracks = album_soup.select("div.most-viewed-video")

        arr_track_names = []

        for track in album_tracks:
            track_name = track.select_one("div.title-wr>a").text.strip()
            arr_track_names.append(track_name)

        track_names_OrderDict = OrderedDict()
        track_names_OrderDict["name"] = album_name
        track_names_OrderDict["date"] = album_date
        track_names_OrderDict["src"] = down_image_path
        track_names_OrderDict["track_length"] = album_trackLength
        track_names_OrderDict["track"] = arr_track_names
        albumInfo_OrderDict[json_key] = [track_names_OrderDict]

    album_OrderDict["album"] = albumInfo_OrderDict
    list_to_json = json.dumps(album_OrderDict, indent=4, ensure_ascii=False)
    return list_to_json
