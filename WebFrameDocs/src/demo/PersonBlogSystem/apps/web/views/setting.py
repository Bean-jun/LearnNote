from django.shortcuts import render, redirect
from django.urls import reverse

from utils.cos import delete_bucket
from apps.web.models import Project


def settings(request, project_id):
    """项目设置"""
    return render(request, 'web/settings.html')


def settings_delete(request, project_id):
    """项目删除"""
    if request.method == 'GET':
        return render(request, 'web/settings_delete.html')

    if request.method == 'POST':
        project_name = request.POST.get('project_name')

        if not project_name or project_name != request.tracer.project.name:
            return render(request, 'web/settings_delete.html', {'error': "项目名错误"})

        # 删除项目
        if request.tracer.user != request.tracer.project.create_user:
            return render(request, 'web/settings_delete.html', {'error': "不是项目创建者，无法删除"})

        # 删除桶文件及桶
        delete_bucket(request.tracer.project.bucket, request.tracer.project.region)

        # 删除数据库文件
        Project.objects.filter(id=request.tracer.project.id).delete()

        # 重定向到项目首页
        return redirect(reverse('web:project_list'))