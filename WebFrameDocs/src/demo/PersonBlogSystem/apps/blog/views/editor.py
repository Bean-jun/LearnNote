from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, redirect, reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django_redis import get_redis_connection
from pypinyin import lazy_pinyin

from apps.blog.forms.editor import NoteForm
from apps.blog.models import Note, Category
from utils.cos import upload_file
from utils.yuque_sync import YuQueConnect


class SyncIndex(View):
    """修改同步到首页"""
    client = get_redis_connection('default')

    def dispatch(self, request, *args, **kwargs):
        # 删除首页视图，让其重新生成
        SyncIndex.client.delete(':1:index')
        return super().dispatch(request, *args, **kwargs)


class EditorView(SyncIndex):
    """图文编辑页"""

    def get(self, request):

        # 用户请求当前分类的文章列表，返回当前列表
        editor_category_list_id = request.GET.get('editor_category_list')
        notes = None
        try:
            category_id = int(editor_category_list_id)
            notes = Note.objects.filter(category_id=category_id).order_by('-create_datetime')
        except Exception as e:
            pass

        # 处理分类列表&不同分类的文章总数
        category = Category.objects.filter(user=request.user)
        category_list = []
        for item in category:
            count = Note.objects.filter(category=item).count()
            # 处理当前分类数量
            setattr(item, 'count', count)
            category_list.append(item)

        # 博客编辑表单
        form = NoteForm(request)

        # 组织上下文
        context = {
            'form': form,
            'category_list': category_list,
            'notes': notes,
        }

        return render(request, 'blog/editor.html', context)

    def post(self, request):
        form = NoteForm(request, data=request.POST, files=request.FILES)

        if form.is_valid():
            image_obj = form.cleaned_data['top_image']

            # 首页图片回传到cos
            # 上传图片
            url = upload_file(bucket=request.user.bucket,
                              image_obj=image_obj,
                              region=request.user.region)

            # 返回数据
            form.instance.top_image = url
            form.instance.author = request.user
            form.save()

            return redirect(reverse('blog:editor'))

        return render(request, 'blog/editor.html', {'form': form})


@method_decorator(csrf_exempt, name='dispatch')
class ImageUploadView(SyncIndex):
    def post(self, request):
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

        # 上传图片
        context['url'] = upload_file(bucket=request.user.bucket,
                                     image_obj=image_obj,
                                     region=request.user.region)

        # 返回数据
        context['success'] = 1

        return JsonResponse(context)


class ModifyView(SyncIndex):
    """图文修改页"""

    def get(self, request, note_id):

        modify_note = Note.objects.filter(author=request.user, id=note_id).first()
        if not modify_note:
            return redirect(reverse('blog:editor'))

        form = NoteForm(request, initial=dict(title=modify_note.title,
                                              category=modify_note.category,
                                              content=modify_note.content))

        # 处理分类列表&不同分类的文章总数
        category = Category.objects.filter(user=request.user)
        category_list = []
        for item in category:
            count = Note.objects.filter(category=item).count()
            # 处理当前分类数量
            setattr(item, 'count', count)
            category_list.append(item)

        # 组织上下文
        context = {
            'form': form,
            'category_list': category_list,
        }

        return render(request, 'blog/editor.html', context)

    def post(self, request, note_id):
        note = Note.objects.get(author=request.user, id=note_id)

        form = NoteForm(request, instance=note, data=request.POST, files=request.FILES)

        if form.is_valid():
            image_obj = form.cleaned_data['top_image']
            file_size = None
            try:
                file_size = image_obj.size
            except FileNotFoundError as e:
                print("文件早已经存在", e.args)

            # 用户需要重新上传图片文件
            if file_size:
                url = upload_file(bucket=request.user.bucket,
                                  image_obj=image_obj,
                                  region=request.user.region)
                form.instance.top_image = url

            # 修改后将状态改为未同步
            form.instance.sync_status = False
            # 返回数据
            form.save()

            return redirect(reverse('blog:editor'))

        return render(request, 'blog/editor.html', {'form': form})


class DeleteView(SyncIndex):
    """文章删除"""

    def get(self, request, note_id):
        Note.objects.filter(author=request.user, id=note_id).delete()

        # 本站删除文章不对语雀平台做任何处理

        return redirect(reverse('blog:editor'))


class SyncView(View):
    """文章同步语雀平台"""

    def get(self, request):
        # 获取文章同步

        note_id = request.GET.get('note_id', -1)

        try:
            note = Note.objects.filter(author=request.user, id=note_id).first()
        except Note.DoesNotExist:
            return JsonResponse({'msg': '文章不存在', 'code': 416})

        # 同步语雀数据
        client = YuQueConnect(settings.YUQUE_TOKEN, settings.HEADERS)

        repos_slug = note.category.repos_slug
        slug = ''.join(lazy_pinyin(note.category.name)) + str(note.id)
        detail = {
            "title": note.title,
            "slug": slug,
            "public": 0,
            "body": note.content,
        }

        if not note.yuque:
            # 创建文档库中文档
            response = client.create_docs(repos_slug, **detail)
        else:
            # 修改文档库中文档
            response = client.update_docs(repos_slug, note.yuque, **detail)

        try:
            yuque_id = response['data']['id']
            print(response)
        except KeyError:
            return JsonResponse({'msg': '同步失败', 'code': 416})

        note.yuque = yuque_id
        note.sync_status = True
        note.save()

        return JsonResponse({'msg': '同步成功', 'code': 200})
