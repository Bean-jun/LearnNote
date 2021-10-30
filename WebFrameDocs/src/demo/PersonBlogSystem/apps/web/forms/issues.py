from django import forms
from django.core.exceptions import ValidationError
from apps.web.forms.bootstrap import BootStrapForm
from apps.web.models import Issues, ProjectUser, IssuesType, Module, IssuesReply, ProjectInvite


class IssuesModelForm(BootStrapForm, forms.ModelForm):
    """问题表单验证"""

    class Meta:
        model = Issues
        exclude = ['project', 'create_user', 'create_datetime', 'modify_datetime']
        widgets = {
            'assign': forms.Select(attrs={"class": 'selectpicker', 'data-live-search=': 'true'}),
            'attention': forms.SelectMultiple(attrs={"class": 'selectpicker',
                                                     'data-live-search=': 'true',
                                                     'data-actions-box=': 'true'}),
            'parent': forms.Select(attrs={"class": 'selectpicker', 'data-live-search=': 'true'}),
        }

    def __init__(self, request, *args, **kwargs):
        super(IssuesModelForm, self).__init__(*args, **kwargs)
        self.request = request

        # 获取当前项目的所有问题类型
        issues_type_list = IssuesType.objects.filter(project=self.request.tracer.project).values_list('id', 'title')
        self.fields['issues_type'].choices = issues_type_list

        # 获取当前项目中所有的模块
        module_list = [('', '没有任何选择项'), ]  # 用于做提示
        module_obj_list = Module.objects.filter(project=self.request.tracer.project).values_list('id', 'title')
        module_list.extend(module_obj_list)

        self.fields['module'].choices = module_list

        # 指派和关注者
        total_user_list = [
            (self.request.tracer.project.create_user.id, self.request.tracer.project.create_user.username), ]  # 用于做提示
        project_user_list = ProjectUser.objects.filter(project=self.request.tracer.project).values_list('user_id',
                                                                                                        'user__username')

        total_user_list.extend(project_user_list)

        self.fields['assign'].choices = [('', '没有任何选择项')] + total_user_list
        self.fields['attention'].choices = total_user_list

        # 当前项目中创建的问题
        parent_list = [('', '没有任何选择项')]
        parent_obj_list = Issues.objects.filter(project=self.request.tracer.project).values_list('id', 'subject')
        parent_list.extend(parent_obj_list)
        self.fields['parent'].choices = parent_list


class IssuesReplyModelForm(BootStrapForm, forms.ModelForm):
    """评论表单验证"""

    class Meta:
        model = IssuesReply
        fields = ['content', 'reply']


class InviteModelForm(BootStrapForm, forms.ModelForm):
    """邀请验证"""

    class Meta:
        model = ProjectInvite
        fields = ['period', 'count']
