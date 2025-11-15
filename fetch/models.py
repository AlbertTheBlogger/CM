from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class WeiboPost(models.Model):
    mid = models.CharField(max_length=50, unique=True, verbose_name="微博ID")
    user_id = models.CharField(max_length=50, verbose_name="用户ID")
    username = models.CharField(max_length=100, verbose_name="用户名")
    time = models.CharField(max_length=100, verbose_name="发布时间")
    text = models.TextField(verbose_name="微博内容")

    def __str__(self):
        return f"{self.username}: {self.text[:50]}"

    class Meta:
        verbose_name = "微博帖子"
        verbose_name_plural = "微博帖子"


class CustomUserManager(BaseUserManager):
    def create_user(self, account, username, password=None, **extra_fields):
        if not account:
            raise ValueError('Users must have an account name')
        user = self.model(
            account=account,
            username=username,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, account, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(account, username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=15, unique=True, verbose_name="用户名")
    account = models.CharField(max_length=20, unique=True, verbose_name="用户账号")
    level = models.SmallIntegerField(verbose_name="用户等级")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # 是否可以登录admin站点

    objects = CustomUserManager()

    USERNAME_FIELD = 'account'  # 登录时使用的字段
    REQUIRED_FIELDS = ['username']  # 创建超级用户时需要额外提供的字段

    def __str__(self):
        return self.username


class Keyword(models.Model):
    keyword = models.CharField(max_length=255, verbose_name="关键词")
    popularity = models.IntegerField(default=0, verbose_name="话题热度")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return self.keyword


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    content = models.TextField(verbose_name="内容")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    keyword = models.ForeignKey(Keyword, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="关键词")

    def __str__(self):
        return self.content


class Reply(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, verbose_name="评论")
    content = models.TextField(verbose_name="回复内容")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return self.content


class Search(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    content = models.TextField(verbose_name="搜索内容")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return self.content


"""以下模块向前端返回"""


class Module(models.Model):
    title = models.CharField(max_length=100)
    icon = models.URLField()  # 或者用 ImageField 存储图片上传路径
    link = models.CharField(max_length=255)

    def __str__(self):
        return self.title