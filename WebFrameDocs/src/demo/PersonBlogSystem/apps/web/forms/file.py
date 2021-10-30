from django import forms
from django.core.exceptions import ValidationError

from apps.web.forms.bootstrap import BootStrapForm

from apps.web.models import FileRepository


class FileFolderModelForm(BootStrapForm, forms.ModelForm):
    class Meta:
        model = FileRepository
        fields = ['name']

    def __init__(self, request, parent_obj, *args, **kwargs):
        super(FileFolderModelForm, self).__init__(*args, **kwargs)
        self.request = request
        self.parent_obj = parent_obj

    def clean_name(self):
        name = self.cleaned_data['name']

        # 判断当前目录下文件夹是否重复
        if self.parent_obj:
            exists = FileRepository.objects.filter(file_type=2,
                                                   name=name,
                                                   project=self.request.tracer.project,
                                                   parent=self.parent_obj).exists()
        else:
            exists = FileRepository.objects.filter(file_type=2,
                                                   name=name,
                                                   project=self.request.tracer.project,
                                                   parent__isnull=True).exists()

        if exists:
            raise ValidationError("文件夹已经存在")

        return name


class FileUploadModelForm(forms.ModelForm):
    """文件上传cos返回校验"""

    class Meta:
        model = FileRepository
        fields = ['name', 'file_size', 'key', 'file_path', 'parent']

    def clean_file_path(self):
        file_path = self.cleaned_data['file_path']

        return 'https:{}'.format(file_path)
