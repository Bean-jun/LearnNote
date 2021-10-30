import datetime
import json

from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import csrf_exempt

from utils.encrypt import uid
from utils.pagination import Pagination
from apps.web.forms.issues import IssuesModelForm, IssuesReplyModelForm, InviteModelForm
from apps.web.models import Issues, IssuesReply, ProjectUser, IssuesType, ProjectInvite, Transaction, PricePolicy


class CheckFilter():
    """组合筛选"""

    def __init__(self, name, data_list, request):
        self.name = name
        self.data_list = data_list
        self.request = request

    def __iter__(self):
        for item in self.data_list:

            # 处理选中问题
            ck = ''
            # 若是用户请求中包含了筛选条件
            value_list = self.request.GET.getlist(self.name)
            if str(item[0]) in value_list:
                ck = 'checked'
                value_list.remove(str(item[0]))
            else:
                value_list.append(str(item[0]))

            # 产生url,在当前URL的基础上增加
            query_dict = self.request.GET.copy()
            query_dict._mutable = True  # 允许修改query_dict
            query_dict.setlist(self.name, value_list)

            if 'page' in query_dict:
                query_dict.pop('page')

            if query_dict.urlencode():
                url = self.request.path + '?' + query_dict.urlencode()
            else:
                url = self.request.path

            html = "<a class='cell' href='{url}'>" \
                   "<input type='checkbox' {ck} />" \
                   "<label>{text}</label>" \
                   "</a>".format(url=url,
                                 ck=ck,
                                 text=item[1])
            yield mark_safe(html)


class SelectFilter():
    """字段筛选"""

    def __init__(self, name, data_list, request):
        self.name = name
        self.data_list = data_list
        self.request = request

    def __iter__(self):
        yield mark_safe("<select class='select2' multiple='multiple' style='width:100%;' >")
        for item in self.data_list:

            selected = ''
            value_list = self.request.GET.getlist(self.name)
            if str(item[0]) in value_list:
                selected = 'selected'
                value_list.remove(str(item[0]))
            else:
                value_list.append(str(item[0]))

            # 产生url,在当前URL的基础上增加
            query_dict = self.request.GET.copy()
            query_dict._mutable = True  # 允许修改query_dict
            query_dict.setlist(self.name, value_list)

            if 'page' in query_dict:
                query_dict.pop('page')

            if query_dict.urlencode():
                url = self.request.path + '?' + query_dict.urlencode()
            else:
                url = self.request.path

            html = "<option value='{url}' {selected}>{text}</option>".format(url=url,
                                                                             selected=selected,
                                                                             text=item[1])
            yield mark_safe(html)

        yield mark_safe("</select>")


def issues(request, project_id):
    """问题栏"""
    if request.method == "GET":
        # 筛选条件 -- 通过get来实现参数筛选
        allow_filter_name = ['issues_type', 'status', 'priority', 'assign', 'attention']
        condition = {}  # 条件
        for name in allow_filter_name:
            value_list = request.GET.getlist(name)

            if not value_list:
                continue

            condition['{}__in'.format(name)] = value_list

        # 分页获取数据
        form = IssuesModelForm(request)

        issues_obj = Issues.objects.filter(project=request.tracer.project).filter(**condition)

        page_object = Pagination(
            current_page=request.GET.get('page'),
            all_count=issues_obj.count(),
            base_url=request.path_info,
            query_params=request.GET,
            per_page=3,
        )
        issues_object_list = issues_obj[page_object.start:page_object.end]

        project_total_user = [(request.tracer.project.create_user_id, request.tracer.project.create_user.username,)]
        join_user = ProjectUser.objects.filter(project_id=project_id).values_list('user_id', 'user__username')
        project_total_user.extend(join_user)

        invite_form = InviteModelForm(data=request.POST)

        context = {
            'form': form,
            'invite_form': invite_form,
            'issues_object_list': issues_object_list,
            'page_html': page_object.page_html(),
            'filter_list': [
                {'title': '问题类型', 'filter': CheckFilter('issues_type',
                                                        IssuesType.objects.filter(project_id=project_id).values_list(
                                                            'id',
                                                            'title'),
                                                        request)},
                {'title': '状态', 'filter': CheckFilter('status', Issues.STATUS_CHOICES, request)},
                {'title': '优先级', 'filter': CheckFilter('priority', Issues.PRIORITY_CHOICES, request)},
                {'title': '指派者', 'filter': SelectFilter('assign', project_total_user, request)},
                {'title': '关注者', 'filter': SelectFilter('attention', project_total_user, request)},
            ]
        }
        return render(request, 'web/issues.html', context)

    if request.method == "POST":
        form = IssuesModelForm(request, data=request.POST)

        if form.is_valid():
            # 添加问题数据
            form.instance.project = request.tracer.project
            form.instance.create_user = request.tracer.user

            form.save()

            return JsonResponse({'code': 200})

        return JsonResponse({'msg': form.errors, 'code': 416})


def issues_detail(request, project_id, issues_id):
    """问题详细"""
    issues_obj = Issues.objects.filter(id=issues_id, project_id=project_id).first()
    form = IssuesModelForm(request, instance=issues_obj)

    context = {
        "form": form,
        'issues_obj': issues_obj,
    }
    return render(request, 'web/issues_detail.html', context)


@csrf_exempt
def issues_record(request, project_id, issues_id):
    """问题的记录"""
    if request.method == "GET":
        reply_list = IssuesReply.objects.filter(issues__project_id=project_id, issues_id=issues_id)

        data_list = []
        for row in reply_list:
            data = {
                'id': row.id,
                'reply_type_text': row.get_reply_type_display(),
                'content': row.content,
                'create_user': row.create_user.username,
                'datetime': row.create_datetime.strftime("%Y-%m-%d %H:%M"),
                'parent_id': row.reply_id
            }
            data_list.append(data)

        return JsonResponse({'code': 200, 'msg': data_list})

    if request.method == "POST":
        """评论回复"""
        form = IssuesReplyModelForm(request.POST)

        if form.is_valid():
            form.instance.issues_id = issues_id
            form.instance.reply_type = 2
            form.instance.create_user = request.tracer.user
            instance = form.save()
            data = {
                'id': instance.id,
                'reply_type_text': instance.get_reply_type_display(),
                'content': instance.content,
                'create_user': instance.create_user.username,
                'datetime': instance.create_datetime.strftime("%Y-%m-%d %H:%M"),
                'parent_id': instance.reply_id
            }
            return JsonResponse({'code': 200, 'msg': data})

        return JsonResponse({'code': 416, 'msg': "评论失败"})


@csrf_exempt
def issues_change(request, project_id, issues_id):
    """修改详细页记录"""

    def create_reply_record(content):
        """创建记录"""
        issues_reply = IssuesReply.objects.create(
            reply_type=1,
            issues=issues_obj,
            create_user=request.tracer.user,
            content=content
        )
        data = {
            'id': issues_reply.id,
            'reply_type_text': issues_reply.get_reply_type_display(),
            'content': issues_reply.content,
            'create_user': issues_reply.create_user.username,
            'datetime': issues_reply.create_datetime.strftime("%Y-%m-%d %H:%M"),
            'parent_id': issues_reply.reply_id
        }

        return data

    post_dict = json.loads(request.body.decode('utf-8'))

    issues_obj = Issues.objects.filter(project_id=project_id, id=issues_id).first()
    name = post_dict.get('name')
    value = post_dict.get('value')

    # 获取当前字段对象
    field_obj = Issues._meta.get_field(name)
    # 1、数据库更新
    # 1.1 文本
    if name in ['subject', 'desc', 'start_date', 'end_date']:
        if not value:
            if not field_obj.null:
                return JsonResponse({'code': 416, 'msg': '您选择的数据不可以是空哦'})
            setattr(issues_obj, name, None)
            issues_obj.save()
            change_record = "{}变更为空".format(field_obj.verbose_name)
        else:
            setattr(issues_obj, name, value)
            issues_obj.save()
            change_record = "{}变更为{}".format(field_obj.verbose_name, value)

        return JsonResponse({'code': 200, 'msg': create_reply_record(change_record)})

    # 1.2 FK字段
    if name in ['issues_type', 'module', 'parent', 'assign']:
        if not value:
            if not field_obj.null:
                return JsonResponse({'code': 416, 'msg': '您选择的数据不可以是空哦'})
            setattr(issues_obj, name, None)
            issues_obj.save()
            change_record = "{}变更为空".format(field_obj.verbose_name)
        else:
            if name == 'assign':
                # 是否是项目创建者
                if value == str(request.tracer.project.create_user_id):
                    instance = request.tracer.project.create_user
                else:
                    project_user_object = ProjectUser.objects.filter(project_id=project_id,
                                                                     user_id=value).first()
                    if project_user_object:
                        instance = project_user_object.user
                    else:
                        instance = None
                if not instance:
                    return JsonResponse({'code': 416, 'msg': "您选择的值不存在"})

                setattr(issues_obj, name, instance)
                issues_obj.save()
                change_record = "{}更新为{}".format(field_obj.verbose_name, str(instance))  # value根据文本获取到内容

            else:
                # 判断用户输入的值是否为当前项目的信息
                instance = field_obj.remote_field.model.objects.filter(project_id=project_id, id=value).first()

                if not instance:
                    return JsonResponse({'code': 416, 'msg': '您选择的数据不存在'})

                setattr(issues_obj, name, instance)
                issues_obj.save()
                change_record = "{}变更为{}".format(field_obj.verbose_name, str(instance))

        return JsonResponse({'code': 200, 'msg': create_reply_record(change_record)})

    # 1.3 choices 字段
    if name in ['priority', 'status', 'mode']:
        selected_text = None
        for key, text in field_obj.choices:
            if str(key) == value:
                selected_text = text
        if not selected_text:
            return JsonResponse({'code': 416, 'msg': "您选择的值不存在"})

        setattr(issues_obj, name, value)
        issues_obj.save()
        change_record = "{}更新为{}".format(field_obj.verbose_name, selected_text)
        return JsonResponse({'code': 200, 'data': create_reply_record(change_record)})

    # 1.4 m2m 字段
    if name == 'attention':
        if not isinstance(value, list):
            return JsonResponse({'code': 416, 'msg': "数据格式错误"})

        if not value:
            # 关注者为空
            issues_obj.attention.set(value)
            issues_obj.save()
            change_record = "{}更新为空".format(field_obj.verbose_name)
            return JsonResponse({'code': 200, 'data': create_reply_record(change_record)})
        else:
            # 有关注者 --- 》 判断用户是否为用户成员
            # 获取当前项目的所有成员
            user_dict = {str(request.tracer.project.create_user_id): request.tracer.project.create_user.username}
            project_user_list = ProjectUser.objects.filter(project_id=project_id)
            for item in project_user_list:
                user_dict[str(item.user_id)] = item.user.username

            username_list = []
            for user_id in value:
                username = user_dict.get(user_id)
                if not username:
                    # 不是项目成员
                    return JsonResponse({'code': 416, 'msg': "用户不存在，请刷新"})
                username_list.append(username)

            issues_obj.attention.set(value)
            issues_obj.save()
            change_record = "{}更新为{}".format(field_obj.verbose_name, ','.join(username_list))

        return JsonResponse({'code': 200, 'data': create_reply_record(change_record)})

    return JsonResponse({'code': 416, 'msg': "error"})


def invite_url(request, project_id):
    """ 生成邀请码 """

    form = InviteModelForm(data=request.POST)
    if form.is_valid():
        """
        1. 创建随机的邀请码
        2. 验证码保存到数据库
        3. 限制：只有创建者才能邀请
        """
        if request.tracer.user != request.tracer.project.create_user:
            form.add_error('period', "无权创建邀请码")
            return JsonResponse({'code': 416, 'error': form.errors})

        random_invite_code = uid(request.tracer.user.id)
        form.instance.project = request.tracer.project
        form.instance.code = random_invite_code
        form.instance.create_user = request.tracer.user
        form.save()

        # 将验邀请码返回给前端，前端页面上展示出来。
        url = "{scheme}://{host}{path}".format(
            scheme=request.scheme,
            host=request.get_host(),
            path=reverse('web:invite_join', kwargs={'code': random_invite_code})
        )

        return JsonResponse({'code': 200, 'data': url})

    return JsonResponse({'code': 416, 'error': form.errors})


def invite_join(request, code):
    """ 访问邀请码 """
    current_datetime = datetime.datetime.now()

    invite_object = ProjectInvite.objects.filter(code=code).first()
    if not invite_object:
        return render(request, 'web/invite_join.html', {'error': '邀请码不存在'})

    if invite_object.project.create_user == request.tracer.user:
        return render(request, 'web/invite_join.html', {'error': '创建者无需再加入项目'})

    exists = ProjectUser.objects.filter(project=invite_object.project, user=request.tracer.user).exists()
    if exists:
        return render(request, 'web/invite_join.html', {'error': '已加入项目无需再加入'})

    # 是否已过期，如果已过期则使用免费额度
    max_transaction = Transaction.objects.filter(user=invite_object.project.create_user).order_by('-id').first()
    if max_transaction.price_policy.category == 1:
        max_member = max_transaction.price_policy.project_member
    else:
        # 暂时不做时效处理
        # if max_transaction.end_time < current_datetime:
        #     free_object = PricePolicy.objects.filter(category=1).first()
        #     max_member = free_object.project_member
        # else:
        max_member = max_transaction.price_policy.project_member

    # 目前所有成员(创建者&参与者）
    current_member = ProjectUser.objects.filter(project=invite_object.project).count()
    current_member = current_member + 1
    if current_member >= max_member:
        return render(request, 'web/invite_join.html', {'error': '项目成员超限，请升级套餐'})

    # 邀请码是否过期
    limit_datetime = invite_object.create_datetime + datetime.timedelta(minutes=invite_object.period)
    if current_datetime > limit_datetime:
        return render(request, 'web/invite_join.html', {'error': '邀请码已过期'})

    # 数量限制
    if invite_object.count:
        if invite_object.use_count >= invite_object.count:
            return render(request, 'web/invite_join.html', {'error': '邀请码数据已使用完'})
        invite_object.use_count += 1
        invite_object.save()

    ProjectUser.objects.create(user=request.tracer.user, project=invite_object.project)

    # 更新项目参与成员
    invite_object.project.join_count += 1
    invite_object.project.save()

    return render(request, 'web/invite_join.html', {'project': invite_object.project})
