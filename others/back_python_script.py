
# def predict(request):
#
#     loginurl = 'https://ln.122.gov.cn/m/login'
#     captchaurl = 'https://ln.122.gov.cn/captcha?nocache='
#
#
#     # model = model_from_json(open(BASE_DIR + '/model/CNN.json').read())
#
#     gov_session = requests.session()
#     img = gov_session.get(captchaurl)
#     temp_img = img.content
#
#     fp = open(MODEL_CAP_ROOT + "test/default.jpg", "wb")
#     fp.write(temp_img)
#     fp.close()
#
#     image = Image.open(MODEL_CAP_ROOT + "test/default.jpg")
#     wide, high = image.size
#     for j in range(wide):
#         image.putpixel((j, 0), (255, 255, 255))
#     for j in range(high):
#         image.putpixel((0, j), (255, 255, 255))
#     X_ = np.empty((1, 32, 90, 3), dtype='float32')
#
#     X_[0] = np.array(image) / 255
#     Y_pred = model.predict(X_, 1, 1)
#     Pred_text = Vocab().one_hot_to_text(Y_pred[0])
#     print(Pred_text)
#
#
#     response = HttpResponse("func(" + json.dumps({'result':Pred_text}) + ")")
#     response["Access-Control-Allow-Origin"] = " *"
#     response["Access-Control-Allow-Methods"] = "POST,GET,OPTIONS"
#     response["Access-Control-Max-Age"] = "1000"
#     response["Access-Control-Allow-Headers"] = "*"
#     return response
#
#
#
# def huilianwang(request):
#
#     captchaurl = 'https://whois.cnnic.cn/validatecode/image.jsp?0.04'
#
#     # model = model_from_json(open(BASE_DIR + '/model/CNN.json').read())
#
#     gov_session = requests.session()
#     img = gov_session.get(captchaurl)
#     temp_img = img.content
#
#     fp = open(MODEL_CAP_ROOT + "test/e997.jpg", "wb")
#     fp.write(temp_img)
#     fp.close()
#
#     image = Image.open(MODEL_CAP_ROOT+"test/e997.jpg")
#     image = image.resize((90, 32), Image.BILINEAR)
#     image.save(MODEL_CAP_ROOT+"test/default-huilianwang-change.jpg")
#     # Lim = img.convert('L')
#
#     wide, high = image.size
#     # for j in range(wide):
#     #     image.putpixel((j, 0), (255, 255, 255))
#     # for j in range(high):
#     #     image.putpixel((0, j), (255, 255, 255))
#     for i in range(wide):
#         for j in range(high):
#             if min(image.getpixel((i, j))) < 240:
#                 image.putpixel((i, j), (0, 0, 0))
#
#     image.save(MODEL_CAP_ROOT+"test/default-huilianwang-2.jpg")
#
#     image = Image.open(MODEL_CAP_ROOT+"test/default-huilianwang-2.jpg")
#     X_ = np.empty((1, 32, 90, 3), dtype='float32')
#
#     X_[0] = np.array(image) / 255
#     Y_pred = model.predict(X_, 1, 1)
#     Pred_text = Vocab().one_hot_to_text(Y_pred[0])
#     print(Pred_text)
#
#     response = HttpResponse("fund(" + json.dumps({'result':Pred_text}) + ")")
#     response["Access-Control-Allow-Origin"] = " *"
#     response["Access-Control-Allow-Methods"] = "POST,GET,OPTIONS"
#     response["Access-Control-Max-Age"] = "1000"
#     response["Access-Control-Allow-Headers"] = "*"
#     return response