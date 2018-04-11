
from xadmin.views import BaseAdminPlugin

class HelloWorldPlugin(BaseAdminPlugin):
    say_hello = False

    # 初始化方法根据 ``say_hello`` 属性值返回
    def init_request(self, *args, **kwargs):
        return bool(self.say_hello)