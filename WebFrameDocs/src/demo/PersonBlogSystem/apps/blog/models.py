from django.contrib.auth.models import AbstractUser
from django.db import models


class UserInfo(AbstractUser):
    """用户表"""
    # username = models.CharField(max_length=32, verbose_name="用户名")
    # email = models.EmailField(max_length=32, verbose_name="邮箱", db_index=True)
    # password = models.CharField(max_length=32, verbose_name="密码")
    is_super = models.BooleanField(default=False, verbose_name="是否为管理员")
    # AbstractUser中的is_superuser 在这部分中使用is_super替代

    image = models.CharField(max_length=256, blank=True, null=True, verbose_name="用户头像")
    bucket = models.CharField(max_length=128, verbose_name="用户文件存储桶")
    region = models.CharField(max_length=32, verbose_name="地区")


class Category(models.Model):
    """分类"""
    user = models.ForeignKey('blog.UserInfo', on_delete=models.CASCADE, verbose_name="用户名")
    name = models.CharField(max_length=32, verbose_name="分类名称")
    repos_slug = models.CharField(max_length=32, verbose_name="语雀知识库slug")
    create_datetime = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return self.name


class Note(models.Model):
    """用户笔记表"""
    author = models.ForeignKey('blog.UserInfo', on_delete=models.CASCADE, verbose_name="作者")
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name="笔记分类")
    title = models.CharField(max_length=32, verbose_name="标题")
    content = models.TextField(verbose_name="内容")
    yuque = models.CharField(max_length=32, default='', verbose_name="语雀知识库文章id")
    # False表明文章创建或者已经修改，True表示文章已经推送语雀平台
    sync_status = models.BooleanField(default=False, verbose_name="同步状态")
    create_datetime = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    modify_datetime = models.DateTimeField(auto_now=True, verbose_name="最后修改时间")
    top_image = models.ImageField(max_length=256, upload_to='note_image/', height_field='', width_field='',
                                  verbose_name="笔记快照")


class Image(models.Model):
    """笔记图片表"""
    note = models.ForeignKey('Note', on_delete=models.CASCADE, verbose_name='笔记')
    image = models.ImageField(upload_to='note/', verbose_name="笔记图片")
    create_datetime = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")


class UserComment(models.Model):
    """用户评论"""
    user = models.ForeignKey('blog.UserInfo', on_delete=models.CASCADE, verbose_name="用户")
    note = models.ForeignKey('Note', on_delete=models.CASCADE, verbose_name="笔记")
    content = models.CharField(max_length=256, verbose_name="评论内容")
    up = models.PositiveIntegerField(default=0, verbose_name="赞")
    down = models.PositiveIntegerField(default=0, verbose_name='踩')
    create_datetime = models.DateTimeField(auto_now_add=True, verbose_name="评论时间")
    is_top = models.BooleanField(default=False, verbose_name="是否置顶")


class Song(models.Model):
    """博客歌单"""
    user = models.ForeignKey('blog.UserInfo', on_delete=models.CASCADE, verbose_name="用户")
    song_id = models.CharField(max_length=64, verbose_name='歌单ID')
    title = models.CharField(max_length=64, verbose_name="歌单标题")
    is_play = models.BooleanField(default=False, verbose_name="是否首页播放")
