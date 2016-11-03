from django.core.exceptions import ValidationError
from rest_framework import mixins, permissions, viewsets
from rest_framework.response import Response

from api.serializers import CountrySerializer, DomainSerializer,  PubSerializer, ProviderSerializer, PrListSerializer
from api.models import Pub, Country, Domain, Provider, PrList


class CountryViewSet(viewsets.GenericViewSet,
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class DomainViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin):
    queryset = Domain.objects.all()
    serializer_class = DomainSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class PubViewSet(viewsets.GenericViewSet,
                 mixins.ListModelMixin,
                 mixins.RetrieveModelMixin,
                 mixins.CreateModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.DestroyModelMixin):
    queryset = Pub.objects.all()
    serializer_class = PubSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class ProviderViewSet(viewsets.GenericViewSet,
                      mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.CreateModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class PrListViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin):
    queryset = PrList.objects.all()
    serializer_class = PrListSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
