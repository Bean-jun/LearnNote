from django.forms import RadioSelect

class ColorRadioSelect(RadioSelect):
    # 原插件
    # template_name = 'django/forms/widgets/radio.html'
    # option_template_name = 'django/forms/widgets/radio_option.html'

    # 自定义插件
    template_name = 'widgets/color_radio/radio.html'
    option_template_name = 'widgets/color_radio/radio_option.html'