"""
bootstrap插件样式
"""


class BootStrapForm(object):
    """创建Bootstrap样式"""

    bootstrap_class_exclude = []

    def __init__(self, *args, **kwargs):
        super(BootStrapForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():

            if name in self.bootstrap_class_exclude:
                continue

            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = "请输入{}".format(field.label)