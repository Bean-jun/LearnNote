from django import forms
from django.forms.utils import ValidationError

from apps.blog.forms.bootstrap import BootStrapForm
from apps.blog.models import Category


class CategoryModelForm(BootStrapForm, forms.ModelForm):
    """博客分类"""

    class Meta:
        model = Category
        fields = ['name']

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.request = request

    def clean_name(self):
        """判断是否重复添加"""
        name = self.cleaned_data['name']

        exists = Category.objects.filter(user=self.request.user, name=name).exists()

        if exists:
            raise ValidationError("分类重复添加")

        return name