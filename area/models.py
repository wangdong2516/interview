from django.db import models
from model_utils.fields import StatusField
from model_utils import Choices
from model_utils.fields import MonitorField
from model_utils.fields import SplitField
from model_utils.fields import UUIDField
from model_utils.fields import UrlsafeTokenField
# Create your models here.


class ProvinceModel(models.Model):
    """
        省模型类
    """

    id = models.BigAutoField(primary_key=True)
    province_name = models.CharField(
        '省份名称', max_length=64, null=False, blank=False, unique=True, db_index=True
    )

    class Meta:
        db_table = 'province'

    def __str__(self):
        return self.province_name


class CityModel(models.Model):
    """
        市模型类
    """

    id = models.BigAutoField(primary_key=True)
    city_name = models.CharField('市名称', max_length=64, null=False, blank=False, db_index=True)
    province_id = models.ForeignKey(
        ProvinceModel, on_delete=models.DO_NOTHING, null=False, blank=False, db_index=True,
        db_column='province_id', related_name='cities'
    )

    class Meta:
        db_table = 'city'

    def __str__(self):
        return self.city_name


class CountyModel(models.Model):
    """
        区(县)模型类
    """

    id = models.BigAutoField(primary_key=True)
    county_name = models.CharField('区(县)名称', max_length=64, null=False, blank=False, db_index=True)
    city_id = models.ForeignKey(
        CityModel, on_delete=models.DO_NOTHING, null=False, blank=False, db_index=True,
        db_column='city_id', related_name='counties'
    )

    class Meta:
        db_table = 'county'

    def __str__(self):
        return self.county_name


class TownModel(models.Model):
    """
        乡(镇)模型类
    """

    id = models.BigAutoField(primary_key=True)
    town_name = models.CharField('乡(镇)名称', max_length=64, null=False, blank=False, db_index=True)
    county_id = models.ForeignKey(
        CountyModel, on_delete=models.DO_NOTHING, null=False, blank=False, db_index=True,
        db_column='county_id', related_name='towns'
    )

    class Meta:
        db_table = 'town'

    def __str__(self):
        return self.town_name


class Book(models.Model):

    STATUS = Choices('draft', 'published')
    # StatusField()会在模型类定义的时候，寻找模型类的STATUS属性(默认的)，不定义会报错
    status = StatusField()
    # 也可以通过choices_name指定其他属性的名称
    ANOTHER_CHOICES = Choices('draft', 'published')
    another_field = StatusField(choices_name='ANOTHER_CHOICES')
    # StatusField默认不会建立索引

    # DateTimeField的子类，用于监控另一个字段，当另一个字段发生改变的时候，将
    # 监控字段更新为当前时间
    # 将列表传递给when参数的时候，只有匹配到列表中的指定值之一才会更新
    status_changed = MonitorField(monitor='status', when=['published'])

    # SplitField自动创建一个额外的不可编辑的字段正文摘录来存储摘录。该字段不需要直接访问
    # content:字段的完整内容， excerpt:字段的摘要值(只读)， has_more:如果摘要
    # 和内容不同时为True否则为False
    # 默认寻找的是<!-- split -->标记，并且将标记之前的内容存储，是通过SPLIT_MARKER来设置的
    # 如果在内容中没有找到标记，则前两段(其中段落是由空白行分隔的文本块)将被视为摘录。这个数字可以通过设置SPLIT DEFAULT段落设置来定制
    body = SplitField()

    class Meta:
        db_table = 'book'

