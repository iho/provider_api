from django.core.exceptions import ValidationError
from django.db.models import Q
from rest_framework import mixins, permissions, viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response

from api.models import Country, Domain, PrList, Provider, Pub
from api.serializers import (CountrySerializer, DomainSerializer,
                             MovePrListSerializer, PrListSerializer,
                             ProviderSerializer, PubSerializer)


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

    def _check_if_exist(self, request, object=None):
        pub_ids = request.data["pub_ids"]

        pub_ids_db = Pub.objects.filter(
            id__in=pub_ids).values_list('id', flat=True)

        pub_ids_prlist = (object or self.get_object()
                          ).pubs.all().values_list('id', flat=True)
        errors = []
        update = []
        already_have = []
        for pub_id in pub_ids:
            if pub_id in pub_ids_prlist:
                already_have.append(pub_id)
            elif pub_id not in pub_ids_db:
                errors.append(pub_id)
            else:
                update.append(pub_id)
        return update, errors, already_have

    @detail_route(methods=["PATCH"])
    def add_pubs(self, request, pk=None):
        Through = PrList.pubs.through  # M2M through Django model
        to_add, errors, already_have = self._check_if_exist(request)
        Through.objects.bulk_create(
            [Through(
                pub_id=pub_id,
                prlist_id=pk
            )
                for pub_id in to_add]
        )
        return Response({
            "status": 0,
            "pr_list": PrListSerializer(self.get_object()).data,
            "not_in_db": errors,
            "added": to_add,
            "already_have": already_have,
        })

    @detail_route(methods=["PATCH"])
    def remove_pubs(self, request, pk=None):
        """ {"pub_ids": [1, 2, 3]} """

        updated, errors, already_have = self._check_if_exist(request)
        PrList.pubs.through.objects.filter(
            prlist=pk, pub__in=already_have).delete()
        return Response({
            "status": 0,
            "pr_list": PrListSerializer(self.get_object()).data,
            "not_in_db": errors,
            "not_in_pubs": updated,
            "removed": already_have,
        })

    @list_route(methods=["PATCH"])
    def move(self, request):
        """
           Request format: {"pub_ids": [1, 2, 3], "to": 1, "from": 5}
           pub_ids must exist in db and not contains in destination PrList.pub  

        """
        Through = PrList.pubs.through  # M2M through Django model
        data = MovePrListSerializer(data=request.data)
        if not data.is_valid():
            return Response({
                "errors": data.errors
            })

        try:
            destination = PrList.objects.get(id=request.data['to'])
        except PrList.DoesNotExist:
            return Response({
                "error": "Список з таким id ({}) не существует ".format(request.data['to'])
            })

        try:
            from_ids = PrList.objects.get(
                id=request.data['from']).pubs.all().values_list('id', flat=True)
        except PrList.DoesNotExist:
            return Response({
                "error": "Список з таким id ({}) не существует ".format(request.data['from'])
            })

        to_move, not_in_db, already_have = self._check_if_exist(
            request, object=destination)
        not_in_from = []
        to_remove = []
        for pub_id in from_ids:
            if pub_id in to_move or pub_id in already_have:
                to_remove.append(pub_id)
            else:
                not_in_from.append(pub_id)

        to_move = [x for x in to_move if x in to_remove]

        Through.objects.filter(
            prlist=request.data["from"],
            pub__in=to_remove
        ).delete()  # remove pubs from M2M

        Through.objects.bulk_create(
            [Through(
                pub_id=pub_id,
                prlist_id=request.data["to"]
            )
                for pub_id in to_move]
        )
        return Response({
            "status": 0,
            "to":  PrListSerializer(PrList.objects.get(id=request.data['to'])).data,
            "from": PrListSerializer(PrList.objects.get(id=request.data['from'])).data,
            "not_in_db": not_in_db,
            "not_in_from": not_in_from,
            "moved": to_move,
            "already_have": already_have,
        })
