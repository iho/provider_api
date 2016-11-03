from django.contrib.postgres.fields import JSONField
from django.db import models


class Country(models.Model):
    country_name = models.CharField(max_length=200)

    def __str__(self):
        return self.country_name


class Domain(models.Model):
    domain = models.CharField(max_length=200)
    check_date = models.DateTimeField('check date')

    def __str__(self):
        return self.domain


class Pub(models.Model):
    pub_id = models.IntegerField(default=0)
    source = models.ForeignKey('Provider', on_delete=models.CASCADE)
    domain = models.ForeignKey(Domain, null=True, blank=True, default=None)

    def __str__(self):
        return str(self.pub_id) + " in " + str(self.source)


class Provider(models.Model):
    name = models.SlugField(verbose_name='Код')
    title = models.CharField(verbose_name='Название', max_length=120)
    description = models.TextField(
        verbose_name='Описание', blank=True, null=True)

    config = JSONField()

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = 'Провайдер'
        verbose_name_plural = 'Провайдеры'


class PrList(models.Model):
    BLACK = 1
    WHITE = 2
    LIST_TYPES = (
        (BLACK, "1-блеклист"),
        (WHITE,  "2-вайтлист")
    )
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, verbose_name="Страна")
    source = models.ForeignKey(
        Provider, on_delete=models.CASCADE, verbose_name="Источник")
    pubs = models.ManyToManyField(Pub, verbose_name="Пабы")
    root_list = models.ForeignKey(
        "self", null=True, blank=True, default=None, verbose_name="Родительский список")

    list_name = models.CharField(
        unique=True, max_length=200, verbose_name="Название списка")
    creation_date = models.DateTimeField(
        verbose_name="Дата создания", auto_now_add=True)
    modify_date = models.DateTimeField(verbose_name="Дата обновления")
    list_type = models.SmallIntegerField(
        default=0, verbose_name="Тип списка",
        choices=LIST_TYPES)
    bid = models.FloatField(default=0, verbose_name="Бид")
    list_id_on_src = models.IntegerField(
        default=None, verbose_name="ID в источнике")
    archived = models.BooleanField(default=False, verbose_name="В архиве")

    def __str__(self):
        return "Name: " + self.list_name + ", type:" + str(self.list_type) + ", bid=" + str(self.bid)
