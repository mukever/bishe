

import requests
import json
url = 'https://www.imooc.com/passport/user/verifycheck?verify=8771'
print(json.loads(requests.get(url).content.decode('GB2312')))