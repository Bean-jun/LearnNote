from django.template import Library

register = Library()


@register.simple_tag
def use_space_policy(size):
    if size > 1024:
        size = size / 1024
        return "%.2f GB" % (size)
    else:
        return "%.2f MB" % (size)
