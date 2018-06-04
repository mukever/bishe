import json
import os,django
import shutil

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bishe.settings")# project_name 项目名称
django.setup()

import threading
import time
import traceback

import requests
from datetime import datetime

def getTime():
    # 获得当前系统时间的字符串
    localtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    print('localtime=' + localtime)
    # 系统当前时间年份
    year = time.strftime('%Y', time.localtime(time.time()))
    # 月份
    month = time.strftime('%m', time.localtime(time.time()))
    return year,month
from bishe.settings import MEDIA_CAP_ROOT
from monitor.models import SpiderInfo

class SpiderTest():

    def __init__(self,spider_id,re):
        self.spider_id = spider_id
        self.re = re
    def srartp(self):
        spider = SpiderInfo.objects.filter(id=self.spider_id).first()

        print(spider.name)
        spider_thread = SpiderThreadTest(spider,self.re)
        spider_thread.run()


class SpiderThreadTest(threading.Thread):
    def __init__(self, spider,re):
        try:
            super(SpiderThreadTest, self).__init__()
            self.spider = spider
            self.re =re

        except Exception as e:
            traceback.print_exc()

    def run(self):
        try:

            #### create folder
            year, month = getTime()
            medile_path = self.spider.url.name+'/'+str(year)+'/'+str(month)+'/'
            ###path
            folder_path = MEDIA_CAP_ROOT+medile_path
            folder = os.path.exists(folder_path)
            # print(folder)
            if not folder:
                os.makedirs(folder_path)

            ######download pic
            _session = requests.session()
            for i in range(self.re):
                if i%100==0:
                    print("处理"+str(i))
                img = _session.get(self.spider.url.image_url)
                temp_img = img.content

                ######save pic
                temp_name = str(datetime.now())+ ".jpg"

                fp = open(folder_path + temp_name , "wb")
                fp.write(temp_img)
                fp.close()
                # print(folder_path+temp_name)
                # im = open(path + file, 'rb').read()
                files = {'pic': temp_img}
                data = {'tag': self.spider.url.tag}
                url = 'http://101.200.46.167:8000/api/predict/'
                r = requests.post(url, data=data, files=files)
                s = r.content.decode('utf8')
                import json
                j = json.loads(s)
                rr = j['code'].replace(" ","-")+"_"

                shutil.move(folder_path + temp_name, '/Users/diamond/traindata/'+rr+temp_name)  # 移动文件到目标路径（移动+重命名）
        except Exception as e:
            ### finsish task
            traceback.print_exc()
        finally:
            pass






if __name__ == '__main__':
    # spider1 = SpiderTest(1, 200)
    # spider1.srartp()
    # spider1 = SpiderTest(2,200)
    # spider1.srartp()
    # spider1 = SpiderTest(3, 200)
    # spider1.srartp()
    # spider1 = SpiderTest(4, 200)
    # spider1.srartp()
    spider1 = SpiderTest(6, 10000)
    spider1.srartp()
    # spider1 = SpiderTest(7, 200)
    # spider1.srartp()
    # spider1 = SpiderTest(8, 200)
    # spider1.srartp()


