# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Country, Domain, PrList, Provider, Pub


class CountryAdmin(admin.ModelAdmin):
    list_display = ('id', 'country_name')
admin.site.register(Country, CountryAdmin)


class DomainAdmin(admin.ModelAdmin):
    list_display = ('id', 'domain', 'check_date')
    list_filter = ('check_date',)
admin.site.register(Domain, DomainAdmin)


class PubAdmin(admin.ModelAdmin):
    list_display = ('id', 'pub_id', 'source', 'domain')
    list_filter = ('source', 'domain')
admin.site.register(Pub, PubAdmin)


class ProviderAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'title', 'description', 'config')
    search_fields = ('name',)
admin.site.register(Provider, ProviderAdmin)


class PrListAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'country',
        'source',
        'root_list',
        'list_name',
        'creation_date',
        'modify_date',
        'list_type',
        'bid',
        'list_id_on_src',
        'archived',
    )
    list_filter = (
        'country',
        'source',
        'root_list',
        'creation_date',
        'modify_date',
        'archived',
    )
    raw_id_fields = ('pubs',)
admin.site.register(PrList, PrListAdmin)
