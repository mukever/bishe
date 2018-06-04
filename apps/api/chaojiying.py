#!/usr/bin/env python
# coding:utf-8

import requests
from hashlib import md5


class Chaojiying_Client(object):

    def __init__(self, username, password, soft_id):
        self.username = username
        self.password = md5(password.encode('utf8')).hexdigest()
        self.soft_id = soft_id
        self.base_params = {
            'user': self.username,
            'pass2': self.password,
            'softid': self.soft_id,
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
        }

    def PostPic(self, im, codetype):
        """
        im: 图片字节
        codetype: 题目类型 参考 http://www.chaojiying.com/price.html
        """
        params = {
            'codetype': codetype,
        }
        params.update(self.base_params)
        files = {'userfile': ('ccc.jpg', im)}
        r = requests.post('http://upload.chaojiying.net/Upload/Processing.php', data=params, files=files, headers=self.headers)
        return r.json()

    def ReportError(self, im_id):
        """
        im_id:报错题目的图片ID
        """
        params = {
            'id': im_id,
        }
        params.update(self.base_params)
        r = requests.post('http://upload.chaojiying.net/Upload/ReportError.php', data=params, headers=self.headers)
        return r.json()

def chaojicheck(path,predict,tag_len):
    chaojiying = Chaojiying_Client('mukever', 'abc123456', '96001')
    path = '../中国互联网络信息中心/change.jpg'
    im = open(path, 'rb').read()
    res = chaojiying.PostPic(im, 1004)
    text = res['pic_str']
    right = False
    if res['err_no'] ==0:
        if str.upper(res['pic_str'])==text:
            right =True
    return right;


if __name__ == '__main__':
    chaojiying = Chaojiying_Client('mukever', 'abc123456', '96001')
    path = '../中国互联网络信息中心/change.jpg'
    im = open(path, 'rb').read()
    print (chaojiying.PostPic(im, 1004))

