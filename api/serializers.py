from rest_framework import serializers
from api.models import Country, Domain, Pub, Provider, PrList


class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Country


class DomainSerializer(serializers.ModelSerializer):

    class Meta:
        model = Domain


class PubSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pub


class ProviderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Provider


class PrListSerializer(serializers.ModelSerializer):

    class Meta:
        model = PrList
