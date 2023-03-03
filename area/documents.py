from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import CityModel, ProvinceModel, CountyModel, TownModel


@registry.register_document
class CityDocument(Document):

    class Index:
        name = 'city'
        settings = {'number_of_shards': 2, 'number_of_replicas': 2}

    class Django:
        model = CityModel
        fields = [
            'city_name'
        ]


@registry.register_document
class ProvinceDocument(Document):
    cities = fields.NestedField(properties={
        'city_name': fields.TextField(),
        'counties': fields.NestedField(properties={
            'county_name': fields.TextField(),
            'towns': fields.NestedField(properties={
                'town_name': fields.TextField()
            })
        })
    })

    class Index:
        name = 'province'
        settings = {'number_of_shards': 2, 'number_of_replicas': 2}

    class Django:
        model = ProvinceModel
        fields = [
            'province_name'
        ]
        related_models = [CityModel, CountyModel, TownModel]
