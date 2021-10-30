from rest_framework import serializers

from apps.api.models import Machine


class MachineSerializer(serializers.ModelSerializer):
    """机器信息序列化器"""

    class Meta:
        model = Machine
        fields = "__all__"
