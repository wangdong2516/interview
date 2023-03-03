from elasticsearch_dsl import Q
from rest_framework.generics import ListAPIView
from django_filters import rest_framework as filters
from rest_framework.views import APIView

from area.documents import CityDocument, ProvinceDocument
from area.filters import ProvinceFilter
from area.models import ProvinceModel
from area.serializer import ProvinceSerializer, ESCitySerializer
from rest_framework.response import Response

# Create your views here.


class ProvinceListView(ListAPIView):

    serializer_class = ProvinceSerializer
    queryset = ProvinceModel.objects.order_by('-id').all()
    filterset_class = ProvinceFilter


class ProvinceSearchView(APIView):
    """基于ES实现查找"""

    def get(self, request):
        # 获取查询参数
        query_params = request.query_params
        city_name = query_params.get('city_name', '')
        a = Q('bool', must=[Q('match', cities__city_name=city_name)])
        s = Q('nested', path='cities', query=a)
        search_result = ProvinceDocument.search().query(s)
        # 将elasticsearch的结果转换为django查询集
        queryset = search_result.to_queryset()
        print(queryset)
        res = ProvinceSerializer(queryset, many=True)
        return Response({'data': res.data})
