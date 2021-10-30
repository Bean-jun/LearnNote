import time
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from apps.web import models
from apps.web.forms.project import ProjectForm
from utils.cos import create_bucket
from apps.web.models import IssuesType
from apps.web.models import PricePolicy


def project_list(request):
    """项目列表"""

    if request.method == 'GET':

        exists = PricePolicy.objects.exists()
        if not exists:
            html = """<h1 style="text-align:center">请在个人主页添加至少一条价格策略表哦~</h1>"""
            return HttpResponse(html)

        # 用户创建项目
        form = ProjectForm(request)

        # 查看项目列表
        """
        1、从数据库中获取数 
            自己创建的：已星标、未星标
            自己参与的：已星标、未星标
        2、提取已经星标
            列表 = [我创建的已星标]+[我参与的已星标]
        3、三个列表
            星标、创建、未星标    
        """
        project_dict = {'star': [],
                        'create': [],
                        'join': []
                        }

        # 创建的项目
        create_project_list = models.Project.objects.filter(create_user=request.tracer.user)
        for row in create_project_list:
            if row.star:
                project_dict['star'].append({'value': row, 'type': 'create'})
            else:
                project_dict['create'].append(row)

        # 参与的项目
        join_project_list = models.ProjectUser.objects.filter(user=request.tracer.user)
        for item in join_project_list:
            if item.star:
                project_dict['star'].append({'value': item.project, 'type': 'join'})
            else:
                project_dict['join'].append(item.project)

        return render(request, 'web/project_list.html', {'form': form, 'project_dict': project_dict})

    if request.method == "POST":
        form = ProjectForm(request, request.POST)

        if form.is_valid():
            # 验证成功： 数据库需要存储项目名，颜色，描述，创建者

            # 为创建项目的用户创建桶
            bucket = f"saas-{request.tracer.user.id}-{int(100 * time.time())}-1305490799"
            create_bucket(bucket)
            form.instance.bucket = bucket
            form.instance.region = 'ap-shanghai'

            # form表单中没有create_user,需要手动添加
            form.instance.create_user = request.tracer.user

            # 创建项目
            instance = form.save()

            # 项目初始化问题类型
            issues_type_obj = []
            for item in IssuesType.PROJECT_INIT_LIST:
                issues_type_obj.append(IssuesType(project=instance, title=item))

            # 模型批量添加
            IssuesType.objects.bulk_create(issues_type_obj)

            return JsonResponse({"code": 200, "msg": 'ok'})

        return JsonResponse({"code": 406, "msg": form.errors})


def project_star(request, project_type, project_id):
    if project_type == 'user_create':
        # 用户创建项目添加星标
        models.Project.objects.filter(id=project_id, create_user=request.tracer.user).update(star=True)

    if project_type == 'user_join':
        # 用户加入项目添加星标
        models.ProjectUser.objects.filter(project_id=project_id, user=request.tracer.user).update(star=True)

    return redirect(reverse('web:project_list'))


def project_unstar(request, project_type, project_id):
    if project_type == 'create':
        # 用户创建项目取消星标
        models.Project.objects.filter(id=project_id, create_user=request.tracer.user).update(star=False)

    if project_type == 'join':
        # 用户加入项目取消星标
        models.ProjectUser.objects.filter(project_id=project_id, user=request.tracer.user).update(star=False)

    return redirect(reverse('web:project_list'))
