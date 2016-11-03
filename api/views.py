from django.core.exceptions import ValidationError
from rest_framework import mixins, permissions, viewsets
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route

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


from rest_framework.response import Response


class PrListViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin):
    queryset = PrList.objects.all()
    serializer_class = PrListSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    @detail_route(methods=["PATCH"])
    def add_pubs(self, request, pk=None):
        Through = PrList.pubs.through  # M2M through Django model
        Through.objects.bulk_create(
            [Through(
                pub_id=pub_id,
                prlist_id=pk
            )
                for pub_id in request.data["pub_ids"]]
        )
        return Response({"status": 0, "pr_list": PrListSerializer(self.get_object()).data})

    @detail_route(methods=["PATCH"])
    def remove_pubs(self, request, pk=None):
        """ {"pub_ids": [1, 2, 3]} """
        PrList.pubs.through.objects.filter(
            prlist=pk, pub__in=request.data["pub_ids"]).delete()
        return Response({"status": 0, "pr_list": PrListSerializer(self.get_object()).data})

    @list_route(methods=["PATCH"])
    def move(self, request):
        """
           Request format: {"pub_ids": [1, 2, 3], "to": 1, "from": 5}
           pub_ids must exist in db and not contains in destination PrList.pub  

        """
        Through = PrList.pubs.through  # M2M through Django model
        Through.objects.filter(
            prlist=request.data["from"],
            pub__in=request.data["pub_ids"]).delete()  # remove pubs from M2M
        Through.objects.bulk_create(
            [Through(
                pub_id=pub_id,
                prlist_id=request.data["to"]
            )
                for pub_id in request.data["pub_ids"]]
        )
        return Response({"status": 0,
                         "to":  PrListSerializer(PrList.objects.get(id=request.data['to'])).data,
                         "from":  PrListSerializer(PrList.objects.get(id=request.data['from'])).data
                         })
