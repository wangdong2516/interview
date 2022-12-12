from django_filters import rest_framework as filters


class ProvinceFilter(filters.FilterSet):

    province_name = filters.CharFilter(field_name='province_name', lookup_expr='icontains')
    city_name = filters.CharFilter(field_name='cities__city_name', lookup_expr='icontains')
