from django.db import models
from django.contrib.auth.models import User
from fund.models import Fund, Alarm
from app.models import DATE_TYPE, PERCENT_RELEASED, ModelBase
from comparative.models import Benchmark

class ClientBase(ModelBase):

    class Meta:
        abstract = True

    value_date = models.DateField()
    no_of_units = models.DecimalField(max_digits=20, decimal_places=5,blank=True, null=True, verbose_name="No. of Units")
    euro_nav = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    pending_nav = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    commit = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    drawdown = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    various = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    residual_commit = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    distribution = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    valuation = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    total_value = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    proceed = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    inflow_euro = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    inflow_dollar = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    outflow_euro = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    outflow_dollar = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    delta_valuation = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    delta_flow = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    net_movement = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    irr = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True, verbose_name='IRR')
    performance = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    ytd = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    si = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
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
    previous_nav = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True) #last months nav, is this needed?
    performance_fee_added_back = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)# not being imported by alexi? input form?
    subscription_amount = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    redemption_amount = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    net_movement = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    gross_assets_after_subs_red = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    core_non_core = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)


class Client(ClientBase):
    fund = models.ManyToManyField(Fund, through="SubscriptionRedemption", \
                                                        blank=True, null=True)
    alarm = models.ForeignKey(Alarm, blank=True, null=True, related_name='client_alarm')
    #benchmark = models.ManyToManyField(Benchmark, blank=True, null=True, related_name='client_benchmark')
    manager = models.ForeignKey(User, blank=True, null=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    # this will give you the vars in the model method:
    # Client.objects.all()[0].name.__code__.co_names

    def name(self):
        return u'%s %s' % (self.first_name, self.last_name)

    def __unicode__(self):
        return u'%s, %s' % (self.last_name, self.first_name)

class ClientHistory(ClientBase):
    holding = models.ForeignKey('holding.Holding', blank=True, null=True)
    client = models.ForeignKey(Client)
    date_type = models.CharField(max_length=1, choices=DATE_TYPE)

    class Meta:
        verbose_name = 'Client history'

class SubscriptionRedemption(models.Model):

    SUBSCRIPTION_REDEMPTION=(
        (1,'Subscription'),
        (2,'Redemption'),
    )
    fund = models.ForeignKey(Fund)
    client = models.ForeignKey(Client)
    trade_date = models.DateField()
    input_date = models.DateField()
    no_of_units = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    sub_red = models.SmallIntegerField(choices=SUBSCRIPTION_REDEMPTION)
    euro_nav = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    percent_released = models.SmallIntegerField(choices=PERCENT_RELEASED)


