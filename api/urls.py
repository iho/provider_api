from api.views import CountryViewSet, DomainViewSet, PubViewSet, ProviderViewSet, PrListViewSet
from rest_framework import routers

from django.conf.urls import url, include

router = routers.SimpleRouter()
router.register(r'country', CountryViewSet)
router.register(r'domain', DomainViewSet)
router.register(r'pub', PubViewSet)
router.register(r'provider', ProviderViewSet)
router.register(r'prlist', PrListViewSet)


urlpatterns = [
    url(r'^', include(router.urls)),
]
