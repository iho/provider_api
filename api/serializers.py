from rest_framework import serializers

from api.models import Country, Domain, PrList, Provider, Pub


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

    pub_id = serializers.PrimaryKeyRelatedField(many=True, read_only=False,
                                                queryset=Pub.objects.all(), source='pubs')

    class Meta:
        model = PrList
        fields = (
            'id',
            'country',
            'source',
            'pub_id',
            # 'pubs',
            'root_list',
            'list_name',
            'creation_date',
            'modify_date',
            'list_type',
            'bid',
            'list_id_on_src',
            'archived'
        )


class MovePrListSerializer(serializers.Serializer):
    to = serializers.IntegerField(required=True)
    pub_ids = serializers.ListField(
        child=serializers.IntegerField(), required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['from'] = serializers.IntegerField(required=True)
