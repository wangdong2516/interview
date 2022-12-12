from rest_framework.generics import ListAPIView
from django_filters import rest_framework as filters

from area.filters import ProvinceFilter
from area.models import ProvinceModel
from area.serializer import ProvinceSerializer


# Create your views here.

class ProvinceListView(ListAPIView):

    serializer_class = ProvinceSerializer
    queryset = ProvinceModel.objects.order_by('-id').all()
    filterset_class = ProvinceFilter
