from django.core.exceptions import ValidationError
from django.forms import ModelForm

from apps.web.forms.bootstrap import BootStrapForm
from apps.web.models import PricePolicy


class PricePolicyForm(BootStrapForm, ModelForm):
    """价格策略表单"""

    class Meta:
        model = PricePolicy
        fields = "__all__"

    def clean_create_project(self):
        create_project = self.cleaned_data['create_project']
        if create_project <= 0:
            raise ValidationError("项目数量不能小于等于0")

        return create_project

    def clean_project_member(self):
        project_member = self.cleaned_data['project_member']
        if project_member <= 0:
            raise ValidationError("成员数量不能小于等于0")

        return project_member

    def clean_project_space(self):
        project_space = self.cleaned_data['project_space']
        if project_space <= 0:
            raise ValidationError("空间设置不能小于等于0")

        return project_space

    def clean_single_file_space(self):
        single_file_space = self.cleaned_data['single_file_space']
        if self.cleaned_data['project_space'] < single_file_space:
            raise ValidationError("空间设置异常")

        return single_file_space
