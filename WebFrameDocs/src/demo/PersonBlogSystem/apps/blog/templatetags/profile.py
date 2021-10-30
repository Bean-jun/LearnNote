from django.template import Library
from apps.blog.models import UserInfo as blog_UserInfo

register = Library()


@register.inclusion_tag('inclusion/user_profile_image.html')
def user_profile(request):
    # 注册用户
    user = blog_UserInfo.objects.filter(id=request.user.id).first()
    # 微博用户
    # user_weibo = oauth_UserInfo.objects.filter(id=request.user.id).first()

    if user:
        image = user.image
    # elif user_weibo:
    #     image = user_weibo.image
    else:
        image = None

    return {'url': image}
