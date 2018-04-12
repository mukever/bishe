import json

from django.shortcuts import render

# Create your views here.


#predict
import os
from django.http import HttpResponse, response
import requests
from PIL import Image
from keras.models import model_from_json
from numpy.distutils.conv_template import header

from bishe.settings import MODEL_CAP_ROOT
from .vocab import *



model = model_from_json(open(MODEL_CAP_ROOT+'test/model/CNN.json').read())
model.load_weights(MODEL_CAP_ROOT+'test/model/CNN.h5')

def predict(request):

    loginurl = 'https://ln.122.gov.cn/m/login'
    captchaurl = 'https://ln.122.gov.cn/captcha?nocache='


    # model = model_from_json(open(BASE_DIR + '/model/CNN.json').read())

    gov_session = requests.session()
    img = gov_session.get(captchaurl)
    temp_img = img.content

    fp = open(MODEL_CAP_ROOT + "test/default.jpg", "wb")
    fp.write(temp_img)
    fp.close()

    image = Image.open(MODEL_CAP_ROOT + "test/default.jpg")
    wide, high = image.size
    for j in range(wide):
        image.putpixel((j, 0), (255, 255, 255))
    for j in range(high):
        image.putpixel((0, j), (255, 255, 255))
    X_ = np.empty((1, 32, 90, 3), dtype='float32')

    X_[0] = np.array(image) / 255
    Y_pred = model.predict(X_, 1, 1)
    Pred_text = Vocab().one_hot_to_text(Y_pred[0])
    print(Pred_text)


    response = HttpResponse("func(" + json.dumps({'result':Pred_text}) + ")")
    response["Access-Control-Allow-Origin"] = " *"
    response["Access-Control-Allow-Methods"] = "POST,GET,OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response
    # context = {}
    # context['hello'] = '1234'
