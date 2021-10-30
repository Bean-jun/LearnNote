from datetime import datetime, timedelta

from django.conf import settings
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

from apps.api.models import VisitorRecord
from apps.blog.models import UserInfo
from apps.oauth.models import UserInfoWeiBo
from apps.web.models import Transaction, ProjectUser, Project


class Tracer:
    """封装user和price_policy的数据，便于视图函数访问"""

    def __init__(self):
        self.user = None
        self.price_policy = None
        self.project = None  # 将项目进行封装


class LoginMiddleware(MiddlewareMixin):
    """校验用户是否登录"""

    def process_request(self, request):

        request.tracer = Tracer()

        REMOTE_ADDR = request.META.get("REMOTE_ADDR")
        REMOTE_HOST = request.META.get("REMOTE_HOST")
        VisitorRecord.objects.create(addr=REMOTE_ADDR, host=REMOTE_HOST)

        # 匿名用户
        user = None

        user_id, flag = request.session.get('user_id', [0, 0])

        if flag == "origin":
            # 注册用户
            user = UserInfo.objects.filter(id=user_id).first()

        elif flag == 'weibo':
            # 微博授权用户
            user = UserInfo.objects.filter(username=user_id).first()
            user_info_access = UserInfoWeiBo.objects.filter(user_id=user.id).first()
            today = datetime.now()
            # 验证过期需要重新登录
            if timedelta(seconds=int(user_info_access.expires)) + user_info_access.modify_datetime < today:
                user = None

        # 将获取到的用户放置在request中
        request.user = user
        request.tracer.user = user

        # if user:
        # 获取用户最近的一次交易记录，ID值越大越近
        # _object = Transaction.objects.filter(user=user, status=2).order_by('-id').first()

        # 判断权限已经过期
        # current_datetime = datetime.now()
        # if _object.end_time and _object.end_time < current_datetime:
        #     # 账户权限过期
        #     _object = Transaction.objects.filter(user=user, status=2, price_policy__category=1).first()

        # request.tracer.price_policy = _object.price_policy

    def process_view(self, request, view, args, kwargs):
        """非管理员或者未登录用户，只能看白名单页面"""

        def visual_flag(request, user=None):
            """访问状态处理"""
            if not request.path.split('/')[1] in settings.VISITOR_WHITE_FUNCTION:
                """白名单外的"""
                return False
            else:
                if not user:
                    """访客"""
                    if request.path.split('/')[1] == "service":
                        """访客不允许访问service"""
                        return False
                else:
                    return True

        try:
            if request.user is None or request.tracer.user is None:
                # 未登录用户
                if visual_flag(request, request.user) is False:
                    raise Exception("访客访问页面不存在")
                else:
                    return
            elif request.user.email not in settings.ADMIN_ACCOUNT:
                # 登录普通用户
                if visual_flag(request, request.user) is False:
                    raise Exception("用户访问页面不存在")
            elif request.user.email in settings.ADMIN_ACCOUNT:
                # 登录管理员用户
                pass
        except Exception as e:
            raise Http404

        # 项目路径
        if request.path.startswith('/service/project/'):
            # 处理项目策略--用户拥有的
            _object = Transaction.objects.filter(user=request.user, status=2).order_by('-id').first()
            request.tracer.price_policy = _object.price_policy
            return

        if not request.path.startswith('/service/manage/'):
            return

        # 项目ID
        project_id = kwargs.get('project_id')

        # 处理项目策略--用户加入的项目的权限
        _object = Project.objects.filter(id=project_id).first().create_user.transaction_set.order_by(
            '-create_time').first()

        request.tracer.price_policy = _object.price_policy

        # 判断是否为我创建或者我参加的
        project_obj = Project.objects.filter(create_user=request.tracer.user, id=project_id).first()
        if project_obj:
            request.tracer.project = project_obj
            return

        project_user_obj = ProjectUser.objects.filter(user=request.tracer.user, project_id=project_id).first()
        if project_user_obj:
            request.tracer.project = project_user_obj.project
            return

        # 若是都不满足，重定向到项目管理页面
        return redirect(reverse('service:project_list'))
