from django import forms

from apps.web.models import Wiki
from apps.web.forms.bootstrap import BootStrapForm


class WikiModelForm(BootStrapForm, forms.ModelForm):
    """wiki forms类"""
    class Meta:
        model = Wiki
        exclude = ['project', 'depth']  # 将project depth都给用户屏蔽

    def __init__(self,request, *args, **kwargs):
        super(WikiModelForm, self).__init__(*args, **kwargs)
        self.request = request

        # todo: 注意对choices的操作
        # 找到需要的字段内容进行数据重置
        total_data_list = [('','请选择'),] # 用于做提示
        data_list = Wiki.objects.filter(project=self.request.tracer.project).values_list('id', 'title')  # 找到当前project的存在标题

        total_data_list.extend(data_list)

        # 修改显示字段
        self.fields['parent'].choices = total_data_list