"""
抽象化的bootstrap类，用于对form字段的表单初始化
"""


class BootStrapForm(object):

    bootstrap_class_exclude = []

    def __init__(self, *args, **kwargs):
        super(BootStrapForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():

            if name in self.bootstrap_class_exclude:
                continue

            old_class = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = '{} form-control'.format(old_class)
            field.widget.attrs['placeholder'] = "请输入{}".format(field.label)
