import xadmin
from xadmin import views
from xadmin.layout import Main, Fieldset, Row, Side
from xadmin.plugins.auth import UserAdmin, User
from .models import  UserProfile


# ----- adminx 全局配置
class BaseSetting:
    enable_themes = True
    use_bootswatch = True
    show_bookmarks  = False


class GlobalSettings:
    site_title = '验证码识别系统'
    site_footer = '验证码识别系统'
    menu_style = 'accordion'
    show_bookmarks = False
# ------




'''
 直接修改 xadmin 的源码，即 xadmin/plugins/auth.py 里添加这两行代码
from django.contrib.auth import get_user_model
User = get_user_model()
 就可以代替下面那段代码
'''
# ---
# class UserProfileAdmin(UserAdmin):
#     refresh_times = [5, 2]
#     pass


# 卸载 django 自带的 auth_user
# from django.contrib.auth.models import User
# xadmin.site.unregister(User)


# 继承自定义的 UserProfile 覆盖 django 自带的 auth_user
# xadmin.site.register(UserProfile, UserProfileAdmin)
# --
class UserAdmin(object):
    change_user_password_template = None
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)
    style_fields = {'user_permissions': 'm2m_transfer'}
    model_icon = 'fa fa-user'

    def get_form_layout(self):
        if self.org_obj:
            self.form_layout = (
                Main(
                    Fieldset('',
                             'username', 'password',
                             css_class='unsort no_title'
                             ),
                    Fieldset(_('Personal info'),
                             Row('first_name', 'last_name'),
                             'email'
                             ),
                    Fieldset(_('Permissions'),
                             'groups', 'user_permissions'
                             ),
                    Fieldset(_('Important dates'),
                             'last_login', 'date_joined'
                             ),
                ),
                Side(
                    Fieldset(_('Status'),
                             'is_active', 'is_staff', 'is_superuser',
                             ),
                )
            )
        return super(UserAdmin, self).get_form_layout()


xadmin.site.unregister(User)
xadmin.site.register(UserProfile, UserAdmin)

xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)
