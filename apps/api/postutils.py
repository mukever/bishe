from api.chaojiying import Chaojiying_Client
from monitor.models import SpiderInfo, CheckInfo
HEADER = {
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Referer': 'https://hn.122.gov.cn/views/inquiry.html',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
}
def chaojicheck(path,predict,tag_len):
    chaojiying = Chaojiying_Client('mukever', 'abc123456', '96001')
    im = open(path, 'rb').read()
    res = chaojiying.PostPic(im, '100'+tag_len)
    print(res)
    right = 0
    if res['err_no'] ==0:
        if str.upper(res['pic_str'])==predict:
            right = 1
        else:
            chaojiying.ReportError(res['pic_id'])
    return right

