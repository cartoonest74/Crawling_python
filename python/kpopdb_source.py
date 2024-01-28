from collections import OrderedDict
import json
from img_down import img_down

def artist_debut_output(soup):
    artist_debut =[]
    try:
        artist_debut = soup.select_one('#field_58138051b1cf9').text.strip().split(",")
        debut_yaer = artist_debut[1].strip()
        debut_date = artist_debut[0].split(' ')
        debut_day = debut_date[1].strip()
        
        en_month = ['January','February','March','April','May','June','July','August','September','October','November','December']
        month_toNum = en_month.index(debut_date[0])+1
        debut_month = f'{month_toNum}' if month_toNum >= 10 else f'0{month_toNum}'
        
        artist_debut = "{}-{}-{}".format(debut_yaer, debut_month,debut_day)
    except:
        artist_debut = ''
    
    return artist_debut

# Todo member_info
def member_output(soup):
    arr_member = []
    print("member get--------------")
    # member info 가져오기
    member_OrderedDict =OrderedDict()
    members = soup.select("table#table_1>tbody>tr")
    for index,member in enumerate(members):
        member_stage_name = member.select_one("td:nth-child(2)").text.strip()
        member_full_name = member.select_one("td:nth-child(3)").text.strip()
        member_korean_name = member.select_one("td:nth-child(4)").text.strip()
        member_birth = member.select_one("td:nth-child(6)").text.strip()
        member_contry = member.select_one("td:nth-child(7)").text.strip()
        arr_member.append([member_stage_name,member_full_name,member_korean_name,member_birth,member_contry]) 
    member_OrderedDict["member"]=arr_member
    member_toJson = json.dumps(member_OrderedDict, indent=4, ensure_ascii=False)
    return member_toJson

# Todo sns
def sns_output(soup):
    print("sns------------------------------------")
    arr_sns = []
    snss = soup.select(".vc_col-sm-12>div>div>div.wpb_content_element>div>ul>li")
    if len(snss) <= 0:
        snss = soup.select(".vc_col-sm-12>div>div>div.wpb_content_element>div>p")
    sns_orderedDict =OrderedDict()
    for sns in iter(snss):
        sns_a_list = sns.select('a[rel="noopener"]')

        for index,val in enumerate(sns_a_list):
            sns_href = sns_a_list[index]
            if sns_href == None:
                continue

            sns_href = sns_href["href"]
            if 'vlive' in sns_href:
                continue
            print(sns_href)
            hash_index = sns_href.index("/") +2

            cite_name = sns_href[hash_index:]
            cite_name = cite_name.split('.')
            cite_name = cite_name[0] if "www" not in sns_href else cite_name[1]
            
            print("cite_name = {}".format(cite_name))
            arr_sns.append([cite_name,sns_href])
    sns_orderedDict["sns"] = arr_sns
    sns_tojson = json.dumps(sns_orderedDict,indent=4,ensure_ascii=False)
    return sns_tojson

# Todo mv
def mv_output(soup):
    print("music video ------")
    arr_mv = []
    mv_OrderedDict = OrderedDict()
    music_videos = soup.select("table#table_2>tbody>tr")
    for mv in music_videos:
        mv_title = mv.select_one('td:nth-child(3)').text.strip()
        mv_date = mv.select_one('td:nth-child(2)').text.strip()
        try:
            mv_src = mv.select_one('a[target="_blank"]')['href']
        except:
            mv_src=''
        arr_mv.append([mv_date, mv_title, mv_src])
    mv_OrderedDict['mv'] = arr_mv
    mv_toJson = json.dumps(mv_OrderedDict, indent=4, ensure_ascii=False)
    return mv_toJson

# TODO img
def img_output(soup):
    arr_img = []
    img_OrderdDict = OrderedDict()
    imgs = soup.select("div.fg-item")
    for img in imgs: 
        img_src = img.select_one("figure>a")['href']
        arr_img.append(img_src)
    img_OrderdDict["img"] = arr_img
    img_toJson = json.dumps(img_OrderdDict,indent=4,ensure_ascii=False)
    return img_toJson