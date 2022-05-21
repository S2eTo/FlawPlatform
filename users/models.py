import uuid
import os.path
from datetime import datetime, timedelta

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

from common.models import BaseModels


class User(AbstractUser):
    avatar_default = os.path.join('avatar', 'default.png')

    point = models.IntegerField(default=0.0, verbose_name="用户积分")
    avatar = models.ImageField(upload_to='avatar/%Y/%m',
                               default=avatar_default,
                               blank=True, null=True, verbose_name="头像")

    def is_default_avatar(self):
        return self.avatar == self.avatar_default


class EmailToken(BaseModels):
    key = models.CharField(max_length=255, verbose_name="Token")
    email = models.EmailField(verbose_name='邮箱')
    mode = models.IntegerField(choices=(
        (1, '用户注册'),
        (2, '重置密码')
    ), default=1, verbose_name="Token 类型")
    expiration = models.DateTimeField(blank=False)

    def save(self, *args, **kwargs):
        # 设置过期时间 30 分钟后
        if not self.expiration:
            self.expiration = timezone.now() + timedelta(minutes=int(settings.EMAIL_TOKEN_TIMEOUT))

        # 自动生成唯一 Token
        self.key = "{}-{}".format(datetime.now().strftime('%Y%m%d%H%M%S%f'), uuid.uuid4())
        super(EmailToken, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "邮箱认证 Token"
        verbose_name_plural = verbose_name

    def interval(self) -> bool:
        """
        判断 60 秒内是否已经操作
        """

        return (timezone.now() + timedelta(seconds=-60)) < self.update_time

    def is_expiration(self) -> bool:
        """
        判断是否过期
        """

        return timezone.now() > self.expiration

    @classmethod
    def remove_expired(cls):
        """
        删除已过期的 Token
        """

        cls.objects.filter(expiration__lte=timezone.now()).delete()
