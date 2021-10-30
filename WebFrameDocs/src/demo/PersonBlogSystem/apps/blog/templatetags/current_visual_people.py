"""
页脚浏览人数显示
"""
from django.template import Library
from apps.api.models import VisitorRecord

register = Library()


@register.inclusion_tag("inclusion/current_visual.html")
def current_visual(request):
    count = VisitorRecord.objects.all().count()
    return {"count": count}
