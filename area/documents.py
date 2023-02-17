from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from .models import CityModel


@registry.register_document
class CityDocument(Document):

    class Index:
        name = 'city'
        settings = {'number_of_shards': 3, 'number_of_replicas': 2}

    class Django:
        model = CityModel
        fields = [
            'city_name'
        ]
