from django.urls import path
from area.views import ProvinceListView, ProvinceSearchView

urlpatterns = [
    path('province_list/', ProvinceListView.as_view()),
    path('province_search/', ProvinceSearchView.as_view()),
]
