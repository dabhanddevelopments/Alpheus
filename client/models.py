from django.db import models
from django.contrib.auth.models import User
from fund.models import Fund, Alarm
from app.models import DATE_TYPE, PERCENT_RELEASED, ModelBase, Currency, YES_NO
from comparative.models import Benchmark

class ClientBase(ModelBase):

    class Meta:
        abstract = True

    value_date = models.DateField(null=True)
    no_of_units = models.DecimalField(max_digits=20, decimal_places=5,null=True, verbose_name="No. of Units")
    euro_nav = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    base_nav = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    mtd = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    ytd = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    si = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    drawdown = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    ann_return1 = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    ann_return3 = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    ann_return5 = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    ann_volatility1 = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    ann_volatility3 = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    ann_volatility5 = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    sharpe_ratio1 = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    sharpe_ratio3 = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    sharpe_ratio5 = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    alpha1 = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    alpha3 = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    alpha5 = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    beta1 = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    beta3 = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    beta5 = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    correlation1 = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    correlation3 = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    correlation5 = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    previous_nav = models.DecimalField(max_digits=20, decimal_places=5, null=True) #last months nav, is this needed?
    performance_fee_added_back = models.DecimalField(max_digits=20, decimal_places=5, null=True)# not being imported by alexi? input form?
    subscription_amount = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    redemption_amount = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    net_movement = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    gross_assets_after_subs_red = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    core_non_core = models.DecimalField(max_digits=20, decimal_places=5, null=True)


class Client(ClientBase):
    fund = models.ManyToManyField(Fund, through="SubscriptionRedemption", \
                                                        null=True)
    currency = models.ForeignKey(Currency, related_name='client_currency', null=True)
    alarm = models.ForeignKey(Alarm, null=True, related_name='client_alarm')
    #benchmark = models.ManyToManyField(Benchmark, null=True, related_name='client_benchmark')
    user = models.ForeignKey(User, null=True)
    first_name = models.CharField(null=True,max_length=50)
    last_name = models.CharField(null=True,max_length=50)
    objective = models.CharField(null=True,max_length=300)
    account_number = models.CharField(max_length=200, null=True)

    class Meta:
        ordering = ['last_name']

    # this will give you the vars in the model method:
    # Client.objects.all()[0].name.__code__.co_names

    def name(self):
        return u'%s %s' % (self.first_name, self.last_name)

    def __unicode__(self):
        return u'%s, %s' % (self.last_name, self.first_name)

class ClientHistory(ClientBase):
    client = models.ForeignKey(Client)
    date_type = models.CharField(null=True,max_length=1, choices=DATE_TYPE)

    class Meta:
        verbose_name = 'Client history'

class SubscriptionRedemption(models.Model):
    INSTRUCTION_TYPE = (
        ('new', 'New'),
        ('amend', 'Amend'),
        ('cancel', 'Cancellation'),
    )
    SUBSCRIPTION_REDEMPTION=(
        (1,'Subscription'),
        (2,'Redemption'),
    )
    fund = models.ForeignKey(Fund, related_name='subred_fund', null=True)
    client = models.ForeignKey(Client, null=True)
    no_of_units = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    sub_red_switch = models.SmallIntegerField(choices=SUBSCRIPTION_REDEMPTION, null=True)
    percent_released = models.SmallIntegerField(choices=PERCENT_RELEASED, null=True)
    instruction_type = models.CharField(max_length=10, choices=INSTRUCTION_TYPE, null=True)
    instruction_date = models.DateField(null=True)
    dealing_date = models.DateField(null=True)
    redemption_date = models.DateField(null=True)
    settlement_date = models.DateField(null=True)
    trade_date = models.DateField(null=True)
    sub_red_price_base = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    sub_red_price_euro = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    sub_red_base_nav = models.DecimalField(max_digits=20, decimal_places=5,verbose_name="NAV", null=True)
    sub_red_euro_nav = models.DecimalField(max_digits=20, decimal_places=5,verbose_name="NAV", null=True)
    full_redemption = models.SmallIntegerField(choices=YES_NO, null=True)
    percent_to_redeem = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    fx_euro = models.DecimalField(max_digits=20, decimal_places=5, null=True)


    def __unicode__(self):
        return u'%s, %s' % (self.fund, self.client)



