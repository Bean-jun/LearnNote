from django.template import Library
from apps.blog.models import Category

register = Library()


@register.inclusion_tag('inclusion/category_navigate.html')
def category_navigate(request):
    """分类导航栏"""
    category_obj = Category.objects.filter(user__is_super=True)
    return {'category_pre': category_obj[:5], 'category_end': category_obj[5:]}
