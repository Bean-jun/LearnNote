from rest_framework import serializers

from apps.blog import models as blog_models


class NoteSerializer(serializers.ModelSerializer):
    """blog中Note序列化器"""
    author = serializers.StringRelatedField(source='author.username')
    category = serializers.StringRelatedField(source='category.name')
    top_image = serializers.URLField()

    class Meta:
        model = blog_models.Note
        fields = "__all__"
