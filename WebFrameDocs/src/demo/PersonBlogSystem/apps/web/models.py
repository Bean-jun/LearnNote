from django.db import models


class PricePolicy(models.Model):
    """SaaS产品价格策略表"""
    CATEGORY_CHOICES = (
        (1, '免费版'),
        (2, '其他'),
    )
    category = models.SmallIntegerField(choices=CATEGORY_CHOICES, default=2, verbose_name="类型")
    title = models.CharField(max_length=32, verbose_name="标题")
    create_project = models.IntegerField(verbose_name="项目数量")
    project_member = models.IntegerField(verbose_name="成员数量")
    project_space = models.IntegerField(verbose_name="项目空间(M)")
    single_file_space = models.IntegerField(verbose_name="单文件空间(M)")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")


class Transaction(models.Model):
    """产品交易订单"""
    ORDER_STATUS_CHOICES = (
        (1, '待支付'),
        (2, '已支付'),
    )
    status = models.SmallIntegerField(choices=ORDER_STATUS_CHOICES, verbose_name="订单状态")
    user = models.ForeignKey('blog.UserInfo', on_delete=models.CASCADE, verbose_name="用户")
    price_policy = models.ForeignKey("PricePolicy", on_delete=models.CASCADE, verbose_name="价格策略")
    count = models.IntegerField(verbose_name="产品数量(年)", help_text="0表示无期限")
    pay_price = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="支付价格")
    start_time = models.DateTimeField(null=True, blank=True, verbose_name="开始时间")
    end_time = models.DateTimeField(null=True, blank=True, verbose_name="结束时间")
    order = models.CharField(max_length=64, unique=True, verbose_name="订单号")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")


class Project(models.Model):
    """项目内容"""
    COLOR_CHOICES = (
        (1, '#ff0c0a'),
        (2, '#ff0aef'),
        (3, '#1d0aff'),
        (4, '#0af4ff'),
        (5, '#1aff0a'),
        (6, '#ffeb0a'),
    )
    name = models.CharField(max_length=64, verbose_name="项目名称")
    desc = models.CharField(max_length=256, null=True, blank=True, verbose_name="描述")
    color = models.SmallIntegerField(choices=COLOR_CHOICES, verbose_name="颜色", default=1)
    star = models.BooleanField(default=False, verbose_name="星标")
    use_space = models.BigIntegerField(default=0, verbose_name="使用空间(字节)")

    join_count = models.IntegerField(default=1, verbose_name="参与人数")
    create_user = models.ForeignKey("blog.UserInfo", on_delete=models.CASCADE, verbose_name="创建者")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    # 创建时添加文件存储桶及地域
    bucket = models.CharField(max_length=128, verbose_name="桶名称")
    region = models.CharField(max_length=32, verbose_name="地域")


class ProjectUser(models.Model):
    """项目参与者"""
    project = models.ForeignKey('Project', on_delete=models.CASCADE, verbose_name="项目名称")
    user = models.ForeignKey("blog.UserInfo", on_delete=models.CASCADE, verbose_name="用户")
    star = models.BooleanField(default=False, verbose_name="星标")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="加入时间")


# 自关联创建wiki表实现多级目录
class Wiki(models.Model):
    """Wiki模型"""
    project = models.ForeignKey("Project", on_delete=models.CASCADE, verbose_name="项目")
    title = models.CharField(max_length=32, verbose_name="标题")
    content = models.TextField(verbose_name="内容")

    # 自关联 related_name='children' 反向关联字段
    parent = models.ForeignKey("Wiki", on_delete=models.CASCADE, null=True, blank=True, verbose_name="父文章",
                               related_name='children')

    # 解决wiki的顺序问题，避免前端显示因先读取子目录导致内容无法显示
    depth = models.IntegerField(verbose_name="深度")

    def __str__(self):
        return self.title


class FileRepository(models.Model):
    """文件夹存储类"""
    FILE_TYPE_CHOICES = (
        (1, '文件'),
        (2, '文件夹')
    )
    project = models.ForeignKey("Project", on_delete=models.CASCADE, verbose_name="项目")
    file_type = models.SmallIntegerField(choices=FILE_TYPE_CHOICES, verbose_name="文件类型")
    name = models.CharField(max_length=32, verbose_name='文件夹名', help_text='文件/文件夹')
    key = models.CharField(max_length=128, null=True, blank=True, verbose_name="存储在cos的key")
    file_size = models.PositiveIntegerField(verbose_name='文件大小(字节)', null=True)
    file_path = models.CharField(max_length=255, null=True, blank=True, verbose_name="文件路径")

    parent = models.ForeignKey("FileRepository", on_delete=models.CASCADE, null=True, blank=True, verbose_name="父级目录",
                               related_name='child')

    update_user = models.ForeignKey("blog.UserInfo", on_delete=models.CASCADE, verbose_name="最近更新者")
    modify_datetime = models.DateTimeField(auto_now=True, verbose_name="更新时间")


class Module(models.Model):
    """功能模块"""
    project = models.ForeignKey("Project", on_delete=models.CASCADE, verbose_name="项目")
    title = models.CharField(max_length=32, verbose_name='模块名称')

    def __str__(self):
        return self.title


class IssuesType(models.Model):
    """问题类型（任务，bug, 功能...）"""
    PROJECT_INIT_LIST = ['任务', '功能', 'bug']  # 项目创建之初创建这三个默认类型
    project = models.ForeignKey("Project", on_delete=models.CASCADE, verbose_name="项目")
    title = models.CharField(max_length=32, verbose_name='模块名称')

    def __str__(self):
        return self.title


class Issues(models.Model):
    """问题"""
    PRIORITY_CHOICES = (
        ('danger', '高'),
        ('warning', '中'),
        ('success', '低'),
    )
    STATUS_CHOICES = (
        (1, '新建'),
        (2, '处理中'),
        (3, '已解决'),
        (4, '已忽略'),
        (5, '待反馈'),
        (6, '已关闭'),
        (7, '重新打开'),
    )
    MODEL_CHOICES = (
        (1, '公开模式'),
        (2, '隐蔽模式'),
    )
    project = models.ForeignKey("Project", on_delete=models.CASCADE, verbose_name="项目")
    issues_type = models.ForeignKey("IssuesType", on_delete=models.CASCADE, verbose_name="问题类型")
    module = models.ForeignKey("Module", on_delete=models.CASCADE, null=True, blank=True, verbose_name="功能模块")
    subject = models.CharField(max_length=32, verbose_name='主题')
    desc = models.TextField(verbose_name='问题描述')
    priority = models.CharField(choices=PRIORITY_CHOICES, max_length=12, default='danger', verbose_name="优先级")
    status = models.SmallIntegerField(choices=STATUS_CHOICES, verbose_name="状态", default=1)
    assign = models.ForeignKey("blog.UserInfo", related_name='task', null=True, blank=True, on_delete=models.CASCADE,
                               verbose_name="指派")
    attention = models.ManyToManyField('blog.UserInfo', related_name='observe', blank=True, verbose_name="关注者")
    start_date = models.DateTimeField(null=True, blank=True, verbose_name="开始时间")
    end_date = models.DateTimeField(null=True, blank=True, verbose_name="结束时间")
    mode = models.SmallIntegerField(choices=MODEL_CHOICES, verbose_name="模式", default=1)
    parent = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="父问题",
                               related_name='child')
    create_user = models.ForeignKey("blog.UserInfo", related_name='create_user', null=True, blank=True,
                                    on_delete=models.CASCADE, verbose_name="创建者")
    create_datetime = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    modify_datetime = models.DateTimeField(verbose_name='最后更新时间', auto_now=True)

    def __str__(self):
        return self.subject


class IssuesReply(models.Model):
    """ 问题回复"""
    reply_type_choices = (
        (1, '修改记录'),
        (2, '回复')
    )
    reply_type = models.IntegerField(verbose_name='类型', choices=reply_type_choices)

    issues = models.ForeignKey('Issues', on_delete=models.CASCADE, verbose_name='问题')
    content = models.TextField(verbose_name='描述')
    create_user = models.ForeignKey('blog.UserInfo', on_delete=models.CASCADE, verbose_name='创建者',
                                    related_name='create_reply')
    create_datetime = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    reply = models.ForeignKey('IssuesReply', on_delete=models.CASCADE, verbose_name='回复', null=True, blank=True)


class ProjectInvite(models.Model):
    """ 项目邀请码 """
    PERIOD_CHOICES = (
        (30, '30分钟'),
        (60, '1小时'),
        (300, '5小时'),
        (1440, '24小时'),
    )
    project = models.ForeignKey('Project', on_delete=models.CASCADE, verbose_name='项目')
    code = models.CharField(verbose_name='邀请码', max_length=64, unique=True)
    count = models.PositiveIntegerField(verbose_name='限制数量', null=True, blank=True, help_text='空表示无数量限制')
    use_count = models.PositiveIntegerField(verbose_name='已邀请数量', default=0)
    period = models.IntegerField(verbose_name='有效期', choices=PERIOD_CHOICES, default=1440)
    create_datetime = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    create_user = models.ForeignKey('blog.UserInfo', on_delete=models.CASCADE, related_name='create_invite',
                                    verbose_name='创建者', )
