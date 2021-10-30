from django import forms
from django.forms.utils import ValidationError

from apps.blog.forms.bootstrap import BootStrapForm
from apps.blog.models import Song
from utils import netease


class SongModelForm(BootStrapForm, forms.ModelForm):
    link = forms.URLField(label="分享链接",
                          widget=forms.URLInput)

    class Meta:
        model = Song
        fields = []

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.request = request

    def clean(self):
        # 校验是否重复添加&&链接是否正确
        link = self.cleaned_data['link']
        song_id = netease.match_id(link)
        song_title = netease.match_title(link)

        if not all([song_id, song_title]):
            raise ValidationError("链接错误啦")

        exists = Song.objects.filter(user=self.request.user, song_id=song_id).exists()
        if exists:
            raise ValidationError("请不要重复添加")

        # 添加数据到cleaned_data中
        self.cleaned_data['song_id'] = song_id
        self.cleaned_data['title'] = song_title
        self.cleaned_data['user'] = self.request.user

        return self.cleaned_data
