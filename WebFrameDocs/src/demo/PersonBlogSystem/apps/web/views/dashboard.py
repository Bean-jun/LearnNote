import collections
import datetime
import time

from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Count

from apps.web.models import Issues, ProjectUser, Project


def dashboard(request, project_id):
    """概览"""

    # 问题的数据处理
    status_dict = {}
    for k, v in Issues.STATUS_CHOICES:
        status_dict[k] = {'text': v, 'count': 0}

    issues_data = Issues.objects.filter(project_id=project_id).values('status').annotate(ct=Count('id'))
    for item in issues_data:
        status_dict[item['status']]['count'] = item['ct']

    # 项目成员
    user_list = ProjectUser.objects.filter(project_id=project_id).values('user_id', 'user__username')

    # 最近问题
    top_ten = Issues.objects.filter(project_id=project_id, assign__isnull=False).order_by('-id')[0:10]

    context = {
        'status_dict': status_dict,
        'user_list': user_list,
        'top_ten_object': top_ten,
    }

    return render(request, 'web/dashboard.html', context)


def issues_chart(request, project_id):
    """产生概览表格数据"""
    today = datetime.datetime.now().date()

    date_dict = collections.OrderedDict()
    for i in range(30):
        date = today - datetime.timedelta(days=i)
        date_dict[date.strftime("%Y-%m-%d")] = [time.mktime(date.timetuple()) * 1000, 0]

    # 获取最近30天的问题创建数量
    res = Issues.objects.filter(project_id=project_id,
                                create_datetime__gte=today - datetime.timedelta(days=30)
                                ).extra(select={'ctime': "DATE_FORMAT(web_issues.create_datetime,'%%Y-%%m-%%d')"}
                                        ).values('ctime').annotate(ct=Count('id'))

    for item in res:
        date_dict[item['ctime']][1] = item['ct']

    return JsonResponse({'code': 200, 'data': list(date_dict.values())})
