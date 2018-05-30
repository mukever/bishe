import requests
from datetime import datetime
from bishe.settings import MEDIA_CAP_ROOT
import os
headers = {'Accept': '*/*',
           'Accept-Language': 'en-US,en;q=0.8',
           'Cache-Control': 'max-age=0',
           'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
           'Connection': 'keep-alive',
           'Referer': 'http://www.baidu.com/'
           }

def SaveImg(url,name):
    path = ''
    # 判断是否存在文件夹如果不存在则创建为文件夹
    folder = os.path.exists(MEDIA_CAP_ROOT)
    if not folder:
        os.makedirs(MEDIA_CAP_ROOT)

    temp_path = name + '.jpg'
    real_path = MEDIA_CAP_ROOT + temp_path
    # print(path)
    img = requests.get(url,headers=headers).content
    file_img = open(real_path,'wb')
    file_img.write(img)
    file_img.close()
    return True,temp_path

