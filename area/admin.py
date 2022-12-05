from django.contrib import admin
from area.models import ProvinceModel
from area.models import CityModel
from area.models import CountyModel
from area.models import TownModel
# Register your models here.


admin.site.register(ProvinceModel)
admin.site.register(CityModel)
admin.site.register(CountyModel)
admin.site.register(TownModel)
