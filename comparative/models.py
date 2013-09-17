from django.db import models
from app.models import ModelBase
from app.models import DATE_TYPE, PERCENT_RELEASED

BENCHMARK_TYPE = (
    ('bloomberg', 'Bloomberg'),
    ('estimate', 'Estimate'),
)


class ComparativeBase(models.Model):

    class Meta:
        abstract = True

    si = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    ytd = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    mtd = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    drawdown = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    ann_return1 = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    ann_return3 = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    ann_return5 = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    ann_volatility1 = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    ann_volatility3 = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    ann_volatility5 = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    sharpe_ratio1 = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    sharpe_ratio3 = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    sharpe_ratio5 = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    alpha1 = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    alpha3 = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    alpha5 = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    beta1 = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    beta3 = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    beta5 = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    correlation1 = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    correlation3 = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    correlation5 = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    value_date = models.DateField()

class Comparative(ComparativeBase):

    description= models.CharField(max_length=200, null=True)
    bloomberg_code = models.CharField(max_length=50)

    name = models.CharField(max_length=50)
    #fund = models.ManyToManyField('fund.Fund', related_name="%(app_label)s_%(class)s_fund", blank=True, null=True)
    holding = models.ManyToManyField('holding.Holding', related_name='%(app_label)s_%(class)s_holding', blank=True, null=True)
    client = models.ManyToManyField('client.Client', related_name='%(app_label)s_%(class)s_client', blank=True, null=True)

    class Meta:
        abstract = True

class Peer(Comparative):
    peer_type = models.CharField(max_length=10, choices=BENCHMARK_TYPE)

class PeerHistory(ComparativeBase):
    peer = models.ForeignKey(Peer)

    class Meta:
        verbose_name = 'Peer history'


class Benchmark(Comparative):
    benchmark_type = models.CharField(max_length=10, choices=BENCHMARK_TYPE)

class BenchmarkHistory(ComparativeBase, ModelBase):
    benchmark = models.ForeignKey(Benchmark)
    date_type = models.CharField(max_length=1, choices=DATE_TYPE)

    class Meta:
        verbose_name = 'Benchmark history'


