from django.template import Library
from django.urls import reverse

from apps.web import models


register = Library()


# 这部分实现类似全局显示
@register.inclusion_tag('inclusion/all_project_list.html')
def all_project_list(request):
    # 获取自己创建所有的项目
    create_project_list = models.Project.objects.filter(create_user=request.tracer.user)

    # 获取自己参见的所有项目
    join_project_list = models.ProjectUser.objects.filter(user=request.tracer.user)

    return {'create': create_project_list, 'join': join_project_list, 'request': request}


# 项目菜单 -- 设置默认选中[就是为了加这一个功能]🤡😅
@register.inclusion_tag('inclusion/manage_menu_list.html')
def manage_menu_list(request):
    data_list = [
        {'title': '概览', 'url': reverse('web:manage:dashboard', kwargs={'project_id': request.tracer.project.id})},
        {'title': '问题', 'url': reverse('web:manage:issues', kwargs={'project_id': request.tracer.project.id})},
        {'title': '统计', 'url': reverse('web:manage:statistics', kwargs={'project_id': request.tracer.project.id})},
        {'title': '文件', 'url': reverse('web:manage:file', kwargs={'project_id': request.tracer.project.id})},
        {'title': 'wiki', 'url': reverse('web:manage:wiki', kwargs={'project_id': request.tracer.project.id})},
        {'title': '设置', 'url': reverse('web:manage:settings', kwargs={'project_id': request.tracer.project.id})},
    ]

    # 若是当前路径为data_list的路径，直接添加class
    for item in data_list:
        if request.path.startswith(item['url']):
            item['class'] = 'active'

    return  {'data_list': data_list}
