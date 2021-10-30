from django import forms

from apps.blog.forms.bootstrap import BootStrapForm
from apps.blog.models import Note, Category


class NoteForm(BootStrapForm, forms.ModelForm):
    """note笔记表单"""
    title = forms.CharField(label='',
                            required=True,
                            min_length=1,
                            max_length=32,
                            error_messages={
                                'min_length': '标题不要太短',
                                'max_length': '标题不要太长',
                                'required': '不可以是空的哦'
                            })

    content = forms.CharField(label='',
                              required=True,
                              min_length=5,
                              error_messages={
                                  'min_length': '内容不要太短',
                                  'required': '不可以是空的哦'
                              },
                              widget=forms.Textarea)

    bootstrap_class_exclude = ['top_image']

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

        # 处理文章分类选择问题
        category_list = [('', '请选择文章分类'), ]
        category = Category.objects.filter(user=self.request.user).values_list('id', 'name')
        category_list.extend(category)

        self.fields['category'].choices = category_list

    class Meta:
        model = Note
        fields = ['title', 'content', 'category', 'top_image']
