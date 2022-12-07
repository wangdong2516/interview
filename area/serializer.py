from rest_framework import serializers


class TownSerializer(serializers.Serializer):

    town_name = serializers.CharField()


class CountySerializer(serializers.Serializer):

    county_name = serializers.CharField()
    towns = TownSerializer(many=True)


class CitySerializer(serializers.Serializer):

    city_name = serializers.CharField()
    counties = CountySerializer(many=True)


class ProvinceSerializer(serializers.Serializer):

    province_name = serializers.CharField()
    cities = CitySerializer(many=True)
