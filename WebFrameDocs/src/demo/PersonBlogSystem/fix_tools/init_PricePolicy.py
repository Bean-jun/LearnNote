import os
import sys
import uuid
from datetime import datetime

import django

# 配置路径

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 将路径添加到环境中
sys.path.append(base_dir)

# 加载项目
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PersonBlog.settings')

# 启动django
django.setup()

from apps.web import models
from apps.blog.models import UserInfo

content_str = """
接下来我们将进行数据的修复工作，这是对于之前0.1版本的用户想要迁移时必须使用的脚本，
若您直接从0.1版之后的版本开始使用，则无需关系此脚本~
请从如下选项中选择(输入数字编号回车即可~)：
1. 初始化免费策略及高级策略版本，并将管理员设置为高级策略用户，用户设置为免费策略用户~
2. 初始化免费策略，管理员和用户都将使用免费策略~
"""
status = input(content_str)

# 免费策略
free_price_policy = models.PricePolicy.objects.create(category=1,
                                                      title="免费用户",
                                                      create_project=2,
                                                      project_member=1,
                                                      project_space=5,
                                                      single_file_space=2)

# 高级策略
price_policy = models.PricePolicy.objects.create(category=2,
                                                 title="高级用户",
                                                 create_project=1000,
                                                 project_member=1000,
                                                 project_space=20480,
                                                 single_file_space=4096)

ADMIN_USER = UserInfo.objects.filter(is_super=True).all()
USER = UserInfo.objects.filter(is_super=False).all()

# 添加权限
start_time = datetime.now()

if status == "2":
    _ = USER + ADMIN_USER
else:
    _ = USER

    # 处理管理员
    for instance in ADMIN_USER:
        models.Transaction.objects.create(status=2,
                                          user=instance,
                                          price_policy=price_policy,
                                          pay_price=0,
                                          count=0,
                                          start_time=start_time,
                                          order=str(uuid.uuid4()),  # 产生随机字符串
                                          create_time=start_time)

for instance in _:
    models.Transaction.objects.create(status=2,
                                      user=instance,
                                      price_policy=free_price_policy,
                                      pay_price=0,
                                      count=0,
                                      start_time=start_time,
                                      order=str(uuid.uuid4()),  # 产生随机字符串
                                      create_time=start_time)
print("初始化完成~")