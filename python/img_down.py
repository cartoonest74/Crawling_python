import requests
import uuid
import os
from collections import OrderedDict
import json
import re
import urllib.request
# base64 decode
import base64
import io
from PIL import Image

def make_dir(arr_dirPath):
    save_path = ''
    for dirpath in arr_dirPath: 
        if not os.path.isdir(dirpath):
            os.mkdir(dirpath)
        save_path = dirpath
    return save_path

def img_down(arr_img_url, arr_dirPath):
    print("img down start!!!")
    arr_down_image=[]
    img_orderDict=OrderedDict()
    save_path = make_dir(arr_dirPath)
    
    # springboot path
    springBoot_path =[]
    springBoot_path = save_path.strip().split("market_crolling")

    extension_reg = re.compile(r'JPG|PNG|JPEG',re.IGNORECASE)
    for url in arr_img_url:
        # file_extension_index = url.rfind(".") +1
        # last_extension_check = url.rfind("?") 

        # file_extension = url[file_extension_index:]
        # if last_extension_check != -1:
        #     file_extension = url[file_extension_index:last_extension_check]
        file_extension = extension_reg.search(url).group()
        file_name = f'{uuid.uuid1()}.{file_extension}'
        full_path = f'{save_path}/{file_name}'

        sql_imgSave_path = f'{springBoot_path[1]}/{file_name}'
        if url.find("base64") == -1:
            request_get = requests.get(url)
            with open(full_path,'wb') as photo:
                photo.write(request_get.content)
        else:
            base64_del_src_num = url.find(",")+1
            base64_del_src = url[base64_del_src_num:]
            imgdata = base64.b64decode(base64_del_src)
            dataBytesIO = io.BytesIO(imgdata)
            image = Image.open(dataBytesIO)
            image.save(f'{save_path}/{file_name}')
            
        arr_down_image.append([sql_imgSave_path])

        print(f"imgsave = {sql_imgSave_path}")
    img_orderDict["img"] = arr_down_image
    down_iamge_json = json.dumps(img_orderDict,indent=4,ensure_ascii=False)
    print("img down compleate!!!!!")
    return down_iamge_json