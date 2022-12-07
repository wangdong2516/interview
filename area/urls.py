from django.urls import path
from area.views import ProvinceListView


urlpatterns = [
    path('province_list/', ProvinceListView.as_view()),
]
