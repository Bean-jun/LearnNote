from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from apps.blog.forms.comment import UserCommentForm
from apps.blog.models import Note, UserComment


class DetailView(View):
    """
    博客详情
    """

    def get(self, request, note_id):
        note = Note.objects.filter(id=note_id).first()
        form = UserCommentForm()
        comments = UserComment.objects.filter(note=note, is_top=False).order_by('-create_datetime')
        top_comments = UserComment.objects.filter(note=note, is_top=True).order_by('-create_datetime')

        context = {
            'note': note,
            'form': form,
            'top_comments': top_comments,
            'comments': comments,
        }
        return render(request, 'blog/detail.html', context)


class CommentsView(View):
    """
    博客评论
    """

    def post(self, request, note_id):
        """保存评论数据"""
        form = UserCommentForm(request.POST)
        note = Note.objects.filter(id=note_id).first()

        if form.is_valid():
            form.instance.user = request.user
            form.instance.note = note
            form.save()
            return JsonResponse({'code': 200})

        return JsonResponse({'code': 416, 'msg': form.errors})


class CommentsOperateView(View):
    """处理评论点赞 点踩 置顶"""

    def get(self, request, note_id, comment_id):
        comment = UserComment.objects.filter(note_id=note_id, id=comment_id).first()
        operate = ['top', 'not_top', 'up', 'down']
        for i in operate:
            if request.GET.get(i, None):
                if i == 'top':
                    comment.is_top = True
                if i == 'not_top':
                    comment.is_top = False
                if i == 'up':
                    comment.up += 1
                if i == 'down':
                    comment.down += 1
                comment.save()

        return redirect(reverse('blog:article', args=(note_id,)))
