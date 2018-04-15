



if __name__ == '__main__':

    s = '{"message":"图片验证码输入错误","code":499}'
    import json
    print(json.loads(s))
    j  = json.loads(s)
    print(j['code'])