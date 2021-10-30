from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from apps.web.forms.wiki import WikiModelForm
from apps.web import models
from utils.encrypt import file_uid

from utils.cos import upload_file


def wiki(request, project_id):
    wiki_id = request.GET.get('wiki_id')
    try:
        wiki_id = int(wiki_id)
    except Exception as e:
        return render(request, 'web/wiki.html')

    # 查看文章详细
    wiki_obj = models.Wiki.objects.filter(id=wiki_id, project_id=project_id).first()

    # 文章首页
    return render(request, 'web/wiki.html', {'wiki_obj': wiki_obj})


def wiki_add(request, project_id):
    """wiki添加"""
    if request.method == 'GET':
        form = WikiModelForm(request)

        return render(request, 'web/wiki_form.html', {'form': form})

    if request.method == "POST":
        form = WikiModelForm(request, data=request.POST)

        if form.is_valid():

            # 这部分中需要将depth加入
            if form.instance.parent:  # 若是表单中存在父级，则子集需要深度depth加1
                form.instance.depth = form.instance.parent.depth + 1
            else:  # 不存在父级，直接设置为1
                form.instance.depth = 1

            form.instance.project = request.tracer.project
            form.save()

            return redirect(reverse('web:manage:wiki', kwargs={'project_id': project_id}))


def wiki_catalog(request, project_id):
    """获取wiki目录"""
    # 这样的获取方式会导致前台页面中先获取到wiki子目录导致无法显示
    # data = models.Wiki.objects.filter(project_id=project_id).values('id', 'title', 'parent_id')

    # 加入深度排序，将根目录设置为1，子目录在根目录基础上递增即可
    data = models.Wiki.objects.filter(project_id=project_id).values('id', 'title', 'parent_id').order_by('depth', 'id')
    return JsonResponse({'code': 200, 'msg': list(data)})


def wiki_modify(request, project_id, wiki_id):
    """修改wiki"""
    if request.method == "GET":
        wiki_obj = models.Wiki.objects.filter(id=wiki_id, project_id=project_id).first()

        if not wiki_obj:
            return redirect(reverse('web:manage:wiki', kwargs={'project_id': project_id}))

        # 使用initial初始化表单
        # form = WikiModelForm(request, initial=dict(title=wiki_obj.title, content=wiki_obj.content, parent=wiki_obj.parent))
        # 或者直接传入wiki对象
        form = WikiModelForm(request, instance=wiki_obj)

        return render(request, 'web/wiki_form.html', {'form': form})

    if request.method == "POST":
        form = WikiModelForm(request, data=request.POST)

        if form.is_valid():
            # 数据验证通过 更新库
            models.Wiki.objects.filter(id=wiki_id, project_id=project_id).update(**form.cleaned_data)

        return redirect(reverse('web:manage:wiki', kwargs={'project_id': project_id})+"?wiki_id=" + str(wiki_id))


def wiki_delete(request, project_id, wiki_id):
    """删除wiki"""
    models.Wiki.objects.filter(id=wiki_id, project_id=project_id).delete()
    return redirect(reverse('web:manage:wiki', kwargs={'project_id': project_id}))


@csrf_exempt
def wiki_upload_img(request, project_id):
    """wiki图片上传"""
    context = {
        # 上传成功success为1，url为上传成功后的返回链接，用于图片显示，message用于提示
        "success": 0,
        "message": None,
        "url": None
    }
    # 图片内容
    image_obj = request.FILES.get('editormd-image-file')

    if not image_obj:
        context['message'] = '文件不存在'
        return JsonResponse(context)

    # 图片名称
    # file_end = image_obj.name.rsplit('.')[-1]
    # key = '{}.{}'.format(file_uid(request.tracer.user.id), file_end)

    # 上传图片
    context['url'] = upload_file(bucket=request.tracer.project.bucket,
                                 image_obj=image_obj,
                                 region=request.tracer.project.region)

    # 返回数据
    context['success'] = 1

    return JsonResponse(context)