from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    org = models.CharField('部门', max_length=128, blank=True)
    telephone = models.CharField('电话', max_length=50, blank=True)
    # 最后修改日期。系统自动生成
    mod_date = models.DateTimeField('最后修改日期', auto_now=True)

    class Meta:
        verbose_name = '用户信息'

    def __str__(self):
        return "{}".format(self.user.__str__())
