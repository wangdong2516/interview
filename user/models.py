import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


# Create your models here.


class Address(models.Model):
    """
        地址模型类
    """

    id = models.BigAutoField(primary_key=True)
    address = models.CharField(max_length=60)
    create_time = models.DateTimeField(default=timezone.now, null=False)

    class Meta:
        db_table = 'address'

    def __str__(self):
        return self.address


class User(AbstractUser):
    """
        用户模型类
    """
    id = models.BigAutoField(primary_key=True)
    is_vip = models.BooleanField('是否为VIP用户', default=False, null=False)
    address = models.ForeignKey(Address, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'user'
