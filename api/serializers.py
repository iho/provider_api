from rest_framework import serializers
from api.models import Country, Domain, Pub, Provider, PrList


class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Country
        fields = '__all__'


class DomainSerializer(serializers.ModelSerializer):

    class Meta:
        model = Domain
        fields = '__all__'


class PubSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pub
        fields = '__all__'


class ProviderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Provider
        fields = '__all__'


class PrListSerializer(serializers.ModelSerializer):

    class Meta:
        model = PrList
        fields = '__all__'
