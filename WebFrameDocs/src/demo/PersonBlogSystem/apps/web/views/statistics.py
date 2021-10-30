import collections

from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render

from apps.web.models import Issues, ProjectUser


def statistics(request, project_id):
    return render(request, 'web/statistics.html')


def statistics_priority(request, project_id):
    """项目饼图"""

    # 找到所有的问题，根据优先级分组，每个优先级的问题数量
    start = request.GET.get('start')
    end = request.GET.get('end')

    # 1.构造字典
    data_dict = collections.OrderedDict()
    for key, text in Issues.PRIORITY_CHOICES:
        data_dict[key] = {'name': text, 'y': 0}

    # 2.去数据查询所有分组得到的数据量
    result = Issues.objects.filter(project_id=project_id, create_datetime__gte=start,
                                   create_datetime__lt=end).values('priority').annotate(ct=Count('id'))

    # 3.把分组得到的数据更新到data_dict中
    for item in result:
        data_dict[item['priority']]['y'] = item['ct']

    return JsonResponse({'code': 200, 'data': list(data_dict.values())})


def statistics_project_user(request, project_id):
    """项目柱状图"""
    start = request.GET.get('start')
    end = request.GET.get('end')

    # 1. 所有项目成员 及 未指派
    all_user_dict = collections.OrderedDict()
    # 项目创建者
    all_user_dict[request.tracer.project.create_user.id] = {
        'name': request.tracer.project.create_user.username,
        'status': {item[0]: 0 for item in Issues.STATUS_CHOICES}
    }
    # 项目未指派成员
    all_user_dict[None] = {
        'name': '未指派',
        'status': {item[0]: 0 for item in Issues.STATUS_CHOICES}
    }
    # 项目参与者
    user_list = ProjectUser.objects.filter(project_id=project_id)
    for item in user_list:
        all_user_dict[item.user_id] = {
            'name': item.user.username,
            'status': {item[0]: 0 for item in Issues.STATUS_CHOICES}
        }

    # 2. 去数据库获取相关的所有问题
    issues = Issues.objects.filter(project_id=project_id, create_datetime__gte=start, create_datetime__lt=end)
    for item in issues:
        if not item.assign:
            all_user_dict[None]['status'][item.status] += 1
        else:
            all_user_dict[item.assign_id]['status'][item.status] += 1

    # 3.获取所有的成员
    categories = [data['name'] for data in all_user_dict.values()]

    # 4.构造字典
    data_result_dict = collections.OrderedDict()
    for item in Issues.STATUS_CHOICES:
        data_result_dict[item[0]] = {'name': item[1], "data": []}

    for key, text in Issues.STATUS_CHOICES:
        # key=1,text='新建'
        for row in all_user_dict.values():
            count = row['status'][key]
            data_result_dict[key]['data'].append(count)

    context = {
        'code': 200,
        'data': {
            'categories': categories,
            'series': list(data_result_dict.values())
        }
    }

    return JsonResponse(context)
