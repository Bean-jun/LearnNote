from django import forms
from django.forms.utils import ValidationError

from apps.blog.forms.bootstrap import BootStrapForm
from apps.blog.models import UserComment


class UserCommentForm(BootStrapForm, forms.ModelForm):
    """用户评论表单"""
    content = forms.CharField(label="评论内容",
                              min_length=1,
                              max_length=256,
                              widget=forms.Textarea)

    class Meta:
        model = UserComment
        fields = ['content']

    def clean_content(self):
        content = self.cleaned_data['content']

        if len(content) > 256:
            raise ValidationError("评论太长，请分多次评论哦！")

        return content
