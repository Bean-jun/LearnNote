import time
import uuid

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from pypinyin import lazy_pinyin

from apps.blog.forms.account import RegisterForm, LoginForm, ModifyPwdForm
from apps.blog.forms.category import CategoryModelForm
from apps.blog.forms.price_policy import PricePolicyForm
from apps.blog.forms.song import SongModelForm
from apps.blog.models import UserInfo, UserComment, Category, Song
from apps.web.models import PricePolicy, Transaction
from utils.cos import create_bucket, upload_file
from utils.yuque_sync import YuQueConnect


class RegisterView(View):
    """用户注册"""

    def get(self, request):

        form = RegisterForm()

        return render(request, 'blog/register.html', {'form': form})

    def post(self, request):

        form = RegisterForm(request.POST)

        # 校验数据--数据格式问题--密码的一致性
        if form.is_valid():
            # 保存数据
            email = form.cleaned_data['email']

            if email in settings.ADMIN_ACCOUNT:
                form.instance.is_super = True  # settings中直接设置管理员账号

                # 管理员账号需要设置存储桶
                bucket = f"PersonBlog-{email.split('@')[0]}{int(1000 * time.time())}-1305490799"
                create_bucket(bucket)
                form.instance.bucket = bucket
                form.instance.region = 'ap-shanghai'

                # 普通用户桶 用于存储普通用户头像  在没有超级管理员之前普通用户不可以上传头像
                # 可能设置多个管理员，这时可能存在重复创建
                try:
                    bucket = settings.TNCENT_BUCKET
                    create_bucket(bucket)
                except Exception as e:
                    pass

                # 获取产品价格策略-最大策略组合
                price_policy = PricePolicy.objects.all().order_by("-create_project")[0]
            else:
                form.instance.is_super = False  # 任何用户注册都是普通用户

                form.instance.bucket = settings.TENCENT_BUCKET
                form.instance.region = settings.TENCENT_REGION

                # 获取产品价格策略
                price_policy = PricePolicy.objects.filter(category=1).first()

            instance = form.save()

            # 添加免费版权限
            from datetime import datetime

            # 添加权限交易记录
            start_time = datetime.now()
            Transaction.objects.create(status=2,
                                       user=instance,
                                       price_policy=price_policy,
                                       pay_price=0,
                                       count=0,
                                       start_time=start_time,
                                       order=str(uuid.uuid4()),  # 产生随机字符串
                                       create_time=start_time)

            return JsonResponse({'code': 200})

        return JsonResponse({'code': 416, 'msg': form.errors})


class ModifyPassword(View):
    """修改密码"""

    def post(self, request):
        form = ModifyPwdForm(request, data=request.POST)
        if form.is_valid():
            new_pwd = form.cleaned_data['new_pwd']

            try:
                user = UserInfo.objects.filter(id=request.user.id).first()
            except UserInfo.DoesNotExist:
                return JsonResponse({'code': 416, 'msg': "账号不存在"})

            # 修改密码
            user.password = new_pwd
            user.save()

            # 清理账户，重新登录
            request.session.flush()

            return JsonResponse({'code': 200, 'msg': "请重新登录账号！"})

        return JsonResponse({'code': 416, 'msg': form.errors})


class LoginView(View):
    """用户登录"""

    def get(self, request):

        form = LoginForm()

        return render(request, 'blog/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)

        # 校验数据--邮箱存在问题--密码的一致性
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = UserInfo.objects.filter(email=email, password=password).first()

            if user:
                # 用户登录成功，做session设置
                request.session['user_id'] = [user.id, 'origin']
                request.session.set_expiry(60 * 60 * 24 * 7)

                return redirect(reverse("blog:index"))
            else:
                # 用户密码错误
                form.add_error('email', '邮箱或者密码错误')

        return render(request, 'blog/login.html', {'form': form})


class LogoutView(View):
    """用户退出"""

    def get(self, request):
        request.session.flush()

        return redirect(reverse('blog:index'))


class ProFileView(View):
    """个人主页"""

    def get(self, request):
        if not request.user:
            return redirect(reverse('blog:index'))

        # 处理用户音乐链接的添加
        song_url = request.GET.get('link')
        if song_url:
            try:
                # https://music.163.com/playlist?id=454995617&userid=326393776
                # https://music.163.com/playlist?id=2919885148&userid=326393776
                song_form = SongModelForm(request, data=request.GET)
                if song_form.is_valid():
                    song_form.cleaned_data.pop('link')
                    # 添加数据库中
                    Song.objects.filter(user=request.user).create(**song_form.cleaned_data)
                    return JsonResponse({'msg': 'ok', 'code': 200})
                else:
                    return JsonResponse({'msg': song_form.errors, 'code': 416})
            except Exception as e:
                # 处理异常
                pass

        # 处理用户音乐的删除&&播放
        action_list = ['play', 'stop', 'delete']
        action_response = request.GET
        if action_response:
            # 获取用户音乐设置，开始处理
            song_obj = Song.objects.filter(user=request.user)
            try:
                for action in action_list:
                    id = action_response.get(action)
                    if action == action_list[0]:
                        # 设置播放
                        song_obj.update(is_play=False)
                        song_obj.filter(id=id).update(is_play=True)
                    if action == action_list[1]:
                        # 设置暂停
                        song_obj.filter(id=id).update(is_play=False)
                    if action == action_list[2]:
                        # 删除
                        song_obj.filter(id=id).first().delete()
                return redirect(reverse('blog:profile'))
            except Exception as e:
                pass

        category = Category.objects.filter(user__is_super=True)
        song = Song.objects.filter(user__is_super=True)  # 歌单展示
        userComment = UserComment.objects.filter(user=request.user). \
            select_related('note').order_by('create_datetime')  # 用户评论
        form = CategoryModelForm(request)
        song_form = SongModelForm(request)
        modify_form = ModifyPwdForm(request)
        price_form = PricePolicyForm()
        price_policy = PricePolicy.objects.all()

        context = {
            'category': category,
            'song': song,
            'form': form,
            'userComment': userComment,
            'song_form': song_form,
            'modify_form': modify_form,
            'price_form': price_form,
            'price_policy': price_policy
        }

        return render(request, 'blog/profile.html', context)

    def post(self, request):
        # 添加博客标签
        form = CategoryModelForm(request, data=request.POST)

        if form.is_valid():
            # 添加分类
            form.instance.user = request.user

            name = form.cleaned_data.get('name')  # 分类名称
            repos_slug = ''.join(lazy_pinyin(name))

            # 创建语雀平台知识库
            client = YuQueConnect(settings.YUQUE_TOKEN, settings.HEADERS)
            repos = {
                "name": name,
                "slug": repos_slug,
                "description": name,
                "public": 0,
                "type": "Book"
            }
            response = client.create_user_repos(**repos)

            if response:
                # 添加语雀平台知识库repos_slug
                form.instance.repos_slug = repos_slug
                form.save()

                return JsonResponse({'msg': 'ok', 'code': 200})

        return JsonResponse({'msg': form.errors, 'code': 416})


class SetPricePolicyView(View):
    """设置价格策略"""

    def post(self, request):
        r = PricePolicyForm(request.POST)
        if r.is_valid():
            r.save()
            return JsonResponse({'code': 200, 'msg': "设置完成！"})

        return JsonResponse({'msg': r.errors, 'code': 416})


@method_decorator(csrf_exempt, name='dispatch')
class UserImage(View):
    """个人头像修改"""

    def post(self, request):
        data = request.FILES.get('image')

        if data:
            # 上传图片
            url = upload_file(bucket=request.user.bucket,
                              image_obj=data,
                              region=request.user.region)

            # 修改用户头像
            UserInfo.objects.filter(email=request.user.email).update(image=url)

        return redirect(reverse('blog:profile'))
