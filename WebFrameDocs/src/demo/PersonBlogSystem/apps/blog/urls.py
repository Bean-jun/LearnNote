from django.urls import path
from apps.blog.views import detail, home, account, editor

app_name = 'blog'

urlpatterns = [
    # 网站首页及详细页
    path('', home.IndexView.as_view(), name="index"),  # 网站首页
    path('category/<int:category_id>/', home.CategoryListView.as_view(), name="category"),  # 网站分类列表页
    path('detail/<int:note_id>/', detail.DetailView.as_view(), name="article"),  # 笔记详情
    path('detail/<int:note_id>/comments/', detail.CommentsView.as_view(), name="comments"),  # 笔记详情评论提交

    # 笔记评论操作
    path('detail/<int:note_id>/commentsOperate/<int:comment_id>/', detail.CommentsOperateView.as_view(), name="comments_operate"),

    # 账户注册登录部分
    path('register/', account.RegisterView.as_view(), name='register'),  # 用户注册
    path('login/', account.LoginView.as_view(), name='login'),  # 用户登录
    path('logout/', account.LogoutView.as_view(), name='logout'),  # 用户退出

    # 个人页
    path('profile/', account.ProFileView.as_view(), name='profile'),  # 个人页
    path('profile/user_image', account.UserImage.as_view(), name='user_image'),  # 个人头像修改
    path('profile/modify_pwd/', account.ModifyPassword.as_view(), name='modify_password'),  # 用户修改密码
    path('profile/setPrice/', account.SetPricePolicyView.as_view(), name='setPrice'),  # 处理SaaS价格策略

    # 文章编辑页
    path('editor/', editor.EditorView.as_view(), name='editor'),  # 用户编辑
    path('modify/<int:note_id>/', editor.ModifyView.as_view(), name='modify'),  # 用户博客修改
    path('delete/<int:note_id>/', editor.DeleteView.as_view(), name='delete'),  # 用户博客删除
    path('sync/', editor.SyncView.as_view(), name='sync'),  # 用户博客同步语雀平台
    path('editor/image_upload/', editor.ImageUploadView.as_view(), name="image_upload"),  # 图片上传
]
