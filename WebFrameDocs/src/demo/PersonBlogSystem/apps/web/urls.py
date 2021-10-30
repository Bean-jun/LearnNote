from django.urls import path, include
from apps.web.views import project, statistics, wiki, file, setting, issues, dashboard

app_name = 'web'

urlpatterns = [
    # path('index/', home.index, name='index'),      # 首页
    #
    # # 价格策略
    # path('price/', home.price, name='price'),
    # path('payment/<int:policy_id>/', home.payment, name='payment'),
    # path('pay/', home.pay, name='pay'),
    # path('pay/pay_notify', home.pay_notify, name='pay_notify'),

    # 项目管理
    path('project/', project.project_list, name='project_list'),   # 项目管理页
    path('project/star/<str:project_type>/<int:project_id>/', project.project_star, name='project_star'),   # 创建星标
    path('project/unstar/<str:project_type>/<int:project_id>/', project.project_unstar, name='project_unstar'),   # 取消星标

    # 项目详细概览 -- 亦可
    path('manage/<int:project_id>/', include(([

            path('statistics/', statistics.statistics, name='statistics'),   # 项目统计
            path('statistics/priority/', statistics.statistics_priority, name='statistics_priority'), # 项目饼图
            path('statistics/project/user/', statistics.statistics_project_user, name='statistics_project_user'),   # 项目柱状图


            # 文件路由
            path('file/', file.file, name='file'),   # 项目文件
            path('file/delete/', file.file_delete, name='file_delete'),   # 删除项目文件
            path('file/post/', file.file_post, name='file_post'),   # 客户端文件上传写入服务端
            path('file/download/', file.file_download, name='file_download'),   # 文件下载
            path('cos/cos_credentials/', file.cos_credentials, name='cos_credentials'),   # 项目文件上传授权

            # wiki路由
            path('wiki/', wiki.wiki, name='wiki'),   # 项目wiki
            path('wiki/add/', wiki.wiki_add, name='wiki_add'),   # 项目wiki添加
            path('wiki/modify/<int:wiki_id>/', wiki.wiki_modify, name='wiki_modify'),   # 项目wiki修改
            path('wiki/delete/<int:wiki_id>/', wiki.wiki_delete, name='wiki_delete'),   # 项目wiki删除
            path('wiki/catalog/', wiki.wiki_catalog, name='wiki_catalog'),   # 项目wiki目录
            path('wiki/upload_img/', wiki.wiki_upload_img, name='wiki_upload_img'),   # 项目wiki图片上传
            # path('wiki/detail/', wiki.wiki_detail, name='wiki_detail'),   # 项目wiki详细

            # 项目设置
            path('settings/', setting.settings, name='settings'),   # 项目设置
            path('settings/delete/', setting.settings_delete, name='settings_delete'),   # 项目删除

            # 项目问题
            path('issues/', issues.issues, name='issues'),  # 项目问题
            path('issues/detail/<int:issues_id>/', issues.issues_detail, name='detail'),  # 项目问题详细
            path('issues/record/<int:issues_id>/', issues.issues_record, name='issues_record'),  # 项目操作记录
            path('issues/change/<int:issues_id>/', issues.issues_change, name='issues_change'),  # 项目问题变更
            path('issues/invite/url/', issues.invite_url, name='invite_url'),   # 项目邀请链接

            # 项目概览
            path('dashboard/', dashboard.dashboard, name='dashboard'),   # 项目概览
            path('dashboard/issues/chart', dashboard.issues_chart, name='issues_chart'),   # 项目概览图表

            ], 'manage',), namespace='manage')
         ),   # 项目设置

    # 加入项目
    path('invite/join/<str:code>/', issues.invite_join, name='invite_join'),    # 用户加入项目

    # account 账户管理模块相关链接
    # path('register/', account.register, name='register'),    # 用户注册
    # path('login/sms/', account.login_sms, name='login_sms'),    # 用户短信登录
    # path('login/', account.login, name='login'),    # 用户账号密码登录
    # path('logout/', account.logout, name='logout'),    # 用户退出
    # path('sms/', account.sms, name='sms'),      # 手机短信处理
    # path('image/code/', account.image_code, name='image_code'),      # 获取图片验证码
]
