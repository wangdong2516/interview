from django.db import models

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


