from rest_framework.generics import ListAPIView

from area.models import ProvinceModel
from area.serializer import ProvinceSerializer


# Create your views here.

class ProvinceListView(ListAPIView):

    serializer_class = ProvinceSerializer

    def get_queryset(self):
        name = self.request.query_params.get('name')
        queryset = ProvinceModel.objects.all()
        if name:
            queryset = ProvinceModel.objects.filter(province_name__contains=name)
        return queryset.order_by('-id').all()
