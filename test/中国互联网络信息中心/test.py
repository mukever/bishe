import numpy as np
import requests
from PIL import Image
#改变图片大小
from bishe.settings import MODEL_CAP_ROOT
from keras.models import model_from_json
from numpy.distutils.conv_template import header

from bishe.settings import MODEL_CAP_ROOT
from apps.api.vocab import *
headers = {'Accept': '*/*',
           'Accept-Language': 'en-US,en;q=0.8',
           'Cache-Control': 'max-age=0',
           'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
           'Connection': 'keep-alive',
           'Referer': 'http://www.baidu.com/'
           }

if __name__ == '__main__':


    model = model_from_json(open(MODEL_CAP_ROOT + 'test/model/CNN.json').read())
    model.load_weights(MODEL_CAP_ROOT + 'test/model/CNN.h5')

    captchaurl = 'https://whois.cnnic.cn/validatecode/image.jsp?0.04'

    # model = model_from_json(open(BASE_DIR + '/model/CNN.json').read())

    gov_session = requests.session()
    img = gov_session.get(captchaurl,headers=headers)
    temp_img = img.content

    fp = open("default-huilianwang.jpg", "wb")
    fp.write(temp_img)
    fp.close()


    image = Image.open("default-huilianwang.jpg")
    image = image.resize((90, 32),Image.BILINEAR)
    # Lim = img.convert('L')

    wide, high = image.size
    # for j in range(wide):
    #     image.putpixel((j, 0), (255, 255, 255))
    # for j in range(high):
    #     image.putpixel((0, j), (255, 255, 255))
    for i in range(wide):
        for j in range(high):
            if min(image.getpixel((i, j))) < 240:
                image.putpixel((i, j), (0, 0, 0))

    image.save("default-huilianwang-change.jpg")

    image = Image.open("default-huilianwang-change.jpg")


    X_ = np.empty((1, 32, 90, 3), dtype='float32')

    X_[0] = np.array(image) / 255
    Y_pred = model.predict(X_, 1, 1)
    Pred_text = Vocab().one_hot_to_text(Y_pred[0])
    print(Pred_text)

