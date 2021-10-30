from django.template import Library

register = Library()


@register.simple_tag
def use_space(size):
    if size > 1024 ** 3:
        size = size / 1024 ** 3
        return "%.2f GB" % (size)
    elif size > 1024 ** 2:
        size = size / 1024 ** 2
        return "%.2f MB" % (size)
    elif size > 1024:
        size = size / 1024
        return "%.2f KB" % (size)
    else:
        return "%d B" % (size)