from rest_framework.viewsets import ModelViewSet

from apps.api.auth.auth import LoginParamAuthentication
from apps.api.serializer.note import NoteSerializer
from apps.blog import models as blog_models


class NoteAPIView(ModelViewSet):
    """
    博客序列化

    list:
    获取note全部内容
    create:
    创建一条note内容
    read:
    读取一条特定note内容
    update:
    更新特定note内容
    partial_update:
    更新特定not部分内容
    destroy:
    删除特定note内容
    """
    queryset = blog_models.Note.objects.all()
    serializer_class = NoteSerializer
    authentication_classes = [LoginParamAuthentication, ]
