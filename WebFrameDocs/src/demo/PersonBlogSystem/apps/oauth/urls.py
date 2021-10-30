from django.urls import path

from apps.oauth.views.weibo import WeiboOAuthView, WeiboLogin

app_name = 'oauth'

urlpatterns = [
    path('weibo/', WeiboLogin.as_view(), name='weibo_login'),  # 微博授权接口
    path('weibo/response', WeiboOAuthView.as_view(), name='weibo'),  # 微博后台处理
]
