from django import forms
from django.core.exceptions import ValidationError

from apps.web.forms import bootstrap
from apps.web.forms.widgets import ColorRadioSelect
from apps.web import models


class ProjectForm(bootstrap.BootStrapForm, forms.ModelForm):
    # 这样可以修改desc的属性，不过在下面直接写widgets也可以的
    # desc = forms.CharField(widget=forms.Textarea)

    # 添加此内容，可以让BootStrapForm剔除这部分内容
    bootstrap_class_exclude = ['color']

    class Meta:
        model = models.Project
        fields = ['name', 'color', 'desc']
        widgets = {
            'desc': forms.Textarea,
            'color': ColorRadioSelect(
                attrs={'class': 'color-radio'}
            ),  # 自定义Radio插件
        }

    def __init__(self, request, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.request = request

    def clean_name(self):
        """
        项目校验
        1、校验当前用户是否创建过这个项目
        2、当前用户是否还有额度创建
        """
        name = self.cleaned_data['name']

        # 同一个人创建过相同的项目
        exists = models.Project.objects.filter(name=name, create_user=self.request.tracer.user).exists()

        if exists:
            raise ValidationError("项目重复创建")

        # 用户已经创建的项目个数
        count = models.Project.objects.filter(create_user=self.request.tracer.user).count()

        # 最多创建的项目
        max_count = self.request.tracer.price_policy.create_project

        if count >= max_count:
            raise ValidationError("项目个数超限，请购买套餐")

        return name
