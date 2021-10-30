import json

import requests
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from apps.web.forms.file import FileFolderModelForm, FileUploadModelForm
from apps.web.models import FileRepository
from utils.cos import delete_file, delete_file_list
from utils.cos import credentials


def file(request, project_id):
    """文件列表&添加文件夹"""

    folder_id = request.GET.get('folder', None)
    try:
        folder_id = int(folder_id)
        parent_obj = FileRepository.objects.filter(id=folder_id,
                                                   file_type=2,
                                                   project=request.tracer.project).first()
    except Exception as e:
        parent_obj = None

    if request.method == 'GET':

        # 路径导航
        breadcrumb_list = []
        parent = parent_obj
        while parent:
            breadcrumb_list.append({'id': parent.id, 'name': parent.name})
            parent = parent.parent

        breadcrumb_list.reverse()

        # 查看当前目录下的全部文件夹 & 文件
        queryset = FileRepository.objects.filter(project=request.tracer.project)

        if parent_obj:
            # 其他目录
            file_obj_list = queryset.filter(parent=parent_obj).order_by('-file_type')
        else:
            # 根目录
            file_obj_list = queryset.filter(parent__isnull=True).order_by('-file_type')

        # 用于生成模态框表单
        form = FileFolderModelForm(request, parent_obj)

        context = {
            'form': form,
            'file_obj_list': file_obj_list,
            'breadcrumb_list': breadcrumb_list,
            'folder_obj': parent_obj,  # 当前所在目录对象
        }
        return render(request, 'web/file.html', context)

    if request.method == 'POST':
        # 文件夹的添加和修改

        # 前端传递fid过来，为空就是添加，有值就是修改
        fid = request.POST.get('fid', None)

        try:
            edit_obj = FileRepository.objects.filter(id=int(fid), file_type=2, project=request.tracer.project).first()
        except Exception as e:
            edit_obj = None

        if edit_obj:
            form = FileFolderModelForm(request, parent_obj, data=request.POST, instance=edit_obj)
        else:
            form = FileFolderModelForm(request, parent_obj, data=request.POST)

        if form.is_valid():
            form.instance.update_user = request.tracer.user
            form.instance.project = request.tracer.project
            form.instance.file_type = 2
            form.instance.parent = parent_obj
            form.save()
            return JsonResponse({'code': 200})

        return JsonResponse({'code': 416, 'msg': form.errors})


def file_delete(request, project_id):
    """文件&&文件夹的删除"""
    if request.method == "GET":
        # 获取文件ID
        fid = request.GET.get('fid', None)
        # 删除文件或者文件夹
        delete_obj = FileRepository.objects.filter(id=fid, project=request.tracer.project).first()

        if delete_obj.file_type == 1:
            # 删除文件，需要释放cos

            # 将容量释放
            request.tracer.project.use_space -= delete_obj.file_size
            request.tracer.project.save()

            # cos中删除文件
            delete_file(bucket=request.tracer.project.bucket,
                        key=delete_obj.key,
                        region=request.tracer.project.region)

            # 数据库文件删除
            delete_obj.delete()

            return JsonResponse({'code': 200})

        else:
            # 删除文件夹及文件夹内的文件
            total_size = 0
            key_list = []  # 文件名列表
            folder_list = [delete_obj]

            for folder in folder_list:
                child_list = FileRepository.objects.filter(project=request.tracer.project,
                                                           child=folder).order_by('-file_type')

                for child in child_list:
                    if child.file_type == 2:
                        # 表示文件夹
                        folder_list.append(child)
                    else:
                        # 表示是文件
                        total_size += child.file_size
                        key_list.append({"Key": child.key})

            if key_list:
                # 删除文件
                delete_file_list(bucket=request.tracer.project.bucket,
                                 key_list=key_list,
                                 region=request.tracer.project.region)

            # 释放空间
            request.tracer.project.use_space -= total_size
            request.tracer.project.save()

            # 删除文件夹
            delete_obj.delete()

            return JsonResponse({'code': 200})


@csrf_exempt
def cos_credentials(request, project_id):
    """获取文件上传凭证"""
    # 文件大小限制
    file_list = json.loads(request.body.decode('utf-8'))

    # bug 他人创建的项目文件限制不能限制加入用户~在中间件中对price_policy进行重新封装
    # 单文件最大限制
    single_file_max = request.tracer.price_policy.single_file_space * 1024 * 1024
    # 项目总文件大小限制
    count_file_max = request.tracer.price_policy.project_space * 1024 * 1024
    # 当前总文件
    total_size = 0

    for item in file_list:
        # 单文件限制
        if item['size'] > single_file_max:
            return JsonResponse({'msg': '单文件 {} 超出限制(最大{} M)'.format(item['name'],
                                                                     request.tracer.price_policy.single_file_space),
                                 'code': 416})
        # 项目总文件限制
        total_size += item['size']

    if total_size + request.tracer.project.use_space > count_file_max:
        return JsonResponse({'msg': '上传总文件超出限制(最大{} M)'
                            .format(request.tracer.price_policy.single_file_space),
                             'code': 416})

    data = credentials(request.tracer.project.bucket, request.tracer.project.region)
    return JsonResponse({'data': data, 'code': 200})


@csrf_exempt
def file_post(request, project_id):
    """获取前端文件上传cos回调内容并写入数据库"""
    form = FileUploadModelForm(request.POST)

    if form.is_valid():
        # 校验成功，写入数据库
        data_dic = form.cleaned_data
        data_dic.update({'project': request.tracer.project, 'file_type': 1, 'update_user': request.tracer.user})
        instance = FileRepository.objects.create(**data_dic)

        # 对当前项目空间进行更新
        request.tracer.project.use_space += data_dic['file_size']
        request.tracer.project.save()

        context = {
            'id': instance.id,
            'name': instance.name,
            'file_size': '{} KB'.format(instance.file_size // 1024),
            'username': instance.update_user.username,
            'modify_datetime': instance.modify_datetime.strftime('%Y年%m月%d日 %H:%M'),
        }
        return JsonResponse({'msg': context, 'code': 200})

    return JsonResponse({'msg': "上传失败", 'code': 416})


def file_download(request, project_id):
    """文件下载"""
    fid = request.GET.get('fid', None)

    if not fid:
        return HttpResponse("资源不存在")

    try:
        fid = int(fid)
        file_obj = FileRepository.objects.filter(project=request.tracer.project,
                                                 file_type=1,
                                                 id=fid).first()
    except Exception as e:
        return HttpResponse("资源不存在")

    # 调整资源路径
    file_path = '://'.join(file_obj.file_path.split(':'))

    # iter_content()适应于分批量下载
    res = requests.get(file_path)
    data = res.iter_content()

    # 中文名转义
    from django.utils.encoding import escape_uri_path

    response = HttpResponse(data)
    # 设置请求头以便于下载而不是打开
    response['Content-Disposition'] = "attachment;filename={};".format(escape_uri_path(file_obj.name))

    return response
