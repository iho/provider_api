from django.conf.urls import include, url
from rest_framework import routers

from api.views import (CountryViewSet, DomainViewSet, PrListViewSet,
                       ProviderViewSet, PubViewSet)

router = routers.SimpleRouter()
router.register(r'country', CountryViewSet)
router.register(r'domain', DomainViewSet)
router.register(r'pub', PubViewSet)
router.register(r'provider', ProviderViewSet)
router.register(r'prlist', PrListViewSet)


urlpatterns = [
    url(r'^', include(router.urls)),
]
