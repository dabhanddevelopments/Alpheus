from django.db import models
from django.contrib.auth.models import User, Group
from fund.models import Fund
from client.models import Client
from app.models import (
    ModelBase, DATE_TYPE, FREQUENCY, YES_NO, BUY_SELL,
    SUBSCRIPTION_REDEMPTION, Currency, Country, Fee
)


class Category(models.Model):

    GROUP_ALL = 'all'
    GROUP_SEC = 'sec'
    GROUP_SUB = 'sub'
    GROUP_LOC = 'loc'
    GROUP_INV = 'inv'
    GROUP_ASS = 'ass'
    HOLDING_GROUP = (
        (GROUP_ALL, 'All'),
        (GROUP_SEC, 'Sector'),
        (GROUP_SUB, 'Sub-Sector'),
        (GROUP_LOC, 'Location'),
        (GROUP_INV, 'Investment Type'),
        (GROUP_ASS, 'Asset Class'),
    )

    key = models.CharField(max_length=10, null=True, blank=True)
    name = models.CharField(max_length=50)
    group = models.CharField(max_length=3, choices=HOLDING_GROUP, \
                                                    default=GROUP_ALL)
    def __unicode__(self):
        return self.name

class HoldingBase(ModelBase):

    class Meta:
        abstract = True

    mtd = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    ytd = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    si = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    weight = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    #weight_of_trades #W76 - liquidity adjusted to confirm
    error_range = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    valuation_base = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    base_nav = models.DecimalField(max_digits=20, decimal_places=5,blank=True, null=True, verbose_name="Base NAV")
    euro_nav = models.DecimalField(max_digits=20, decimal_places=5,blank=True, null=True, verbose_name="Euro NAV")
    no_of_units = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    price_of_unit = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    cumulative_nav = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    cumulative_weight = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
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
    cash_flow_euro_amount_euro_dollar = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    cash_flow_percent_euro_dollar = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    valuation_base = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    fx_rate = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    valuation_euro = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    irr = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True, verbose_name='IRR')
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
    interest_rate = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True) #check where used
    ave_purchase_price_base = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    redemption_fee12 = models.DecimalField(max_digits=20, decimal_places=5,\
                                                blank=True, null=True, verbose_name="Redemption Fee 12M")
    redemption_fee24 = models.DecimalField(max_digits=20, decimal_places=5,\
                                                blank=True, null=True, verbose_name="Redemption Fee 24M")
    redemption_fee36 = models.DecimalField(max_digits=20, decimal_places=5,\

                                               blank=True, null=True, verbose_name="Redemption Fee 36M")
    redemption_fee12_percent = models.DecimalField(max_digits=20, decimal_places=5,\
                                                blank=True, null=True, verbose_name="Redemption Fee 12M %")
    redemption_fee24_percent = models.DecimalField(max_digits=20, decimal_places=5,\
                                                blank=True, null=True, verbose_name="Redemption Fee 24M %")
    redemption_fee36_percent = models.DecimalField(max_digits=20, decimal_places=5,\
                                               blank=True, null=True, verbose_name="Redemption Fee 36M %")

    redemption_fee12_euro = models.DecimalField(max_digits=20, decimal_places=5,verbose_name="Redemption Fee 12M")
    redemption_fee24_euro = models.DecimalField(max_digits=20, decimal_places=5,verbose_name="Redemption Fee 12M")
    redemption_fee36_euro = models.DecimalField(max_digits=20, decimal_places=5,verbose_name="Redemption Fee 12M")

    base_price = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    euro_price = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    pending_no_of_units = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    pending_euro_nav = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)

    dealing_date = models.DateField()
    value_date = models.DateField()

class Holding(HoldingBase):
    AMERICAN_EURO = (
        (1, 'American'),
        (2, 'Euro'),
    )
    PUT_CALL = (
        (1, 'Put'),
        (2, 'Call'),
    )
    fund = models.ForeignKey(Fund, blank=True, null=True)
    client = models.ForeignKey(Client, blank=True, null=True)
    currency = models.ForeignKey(Currency, related_name='holding_currency', blank=True, null=True)
    country = models.ForeignKey(Country, related_name='holding_country', blank=True, null=True)
    fee = models.ForeignKey(Fee, related_name='holding_fee', blank=True, null=True)
    counter_party = models.ForeignKey('app.CounterParty', related_name='holding_counter_party', blank=True, null=True)
    sector = models.ForeignKey(Category, related_name='sector', blank=True, null=True)
    sub_sector = models.ForeignKey(Category, related_name='sub_sector', blank=True, null=True)
    location = models.ForeignKey(Category, related_name='location', blank=True, null=True)
    investment_type = models.ForeignKey(Category, related_name='investment_type', blank=True, null=True)
    asset_class = models.ForeignKey(Category, related_name='asset_class', blank=True, null=True)

    name = models.CharField(max_length=50, blank=True, null=True)
    isin = models.CharField(max_length=12, blank=True, null=True)
    rep_code = models.CharField(max_length=50, blank=True, null=True)
    sec_id = models.CharField(max_length=50, blank=True, null=True)
    bloomberg_code = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    valoren = models.IntegerField(blank=True, null=True)
    redemption_frequency = models.SmallIntegerField(choices=FREQUENCY, blank=True, null=True)
    redemption_date = models.DateField(blank=True, null=True)
    redemption_notice = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    max_redemption = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    payment_days = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    gate = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    soft_lock_percent = models.SmallIntegerField(choices=YES_NO, blank=True, null=True)
    soft_lock_date = models.DateField(blank=True, null=True)

    maturity = models.DateField()
    strike = models.DecimalField(max_digits=20, decimal_places=5)
    multiplier = models.DecimalField(max_digits=20, decimal_places=5)
    put_call = models.SmallIntegerField(choices=PUT_CALL)
    american_euro = models.SmallIntegerField(choices=AMERICAN_EURO)
    etf_yes_no = models.SmallIntegerField(choices=YES_NO)
    redemption_cumulative_euro_nav = models.DecimalField(max_digits=20, decimal_places=5)
    redemption_cumulative_weight = models.DecimalField(max_digits=20, decimal_places=5)
    redemption_percent = models.DecimalField(max_digits=20, decimal_places=5)
    redemption_date = models.DateField()

    class Meta:
        ordering = ["id"]

    def __unicode__(self):
        return self.name

class HoldingHistory(HoldingBase):
    holding = models.ForeignKey(Holding)
    date_type = models.CharField(max_length=1, choices=DATE_TYPE)

class CountryBreakdown(models.Model):
    fund = models.ForeignKey(Fund)
    country = models.ForeignKey(Country, related_name='cb_country')
    category = models.ForeignKey(Category, related_name='cb_category')
    mtd = models.DecimalField(max_digits=15, decimal_places=5, blank=True, null=True)
    ytd = models.DecimalField(max_digits=15, decimal_places=5, blank=True, null=True)
    euro_nav = models.DecimalField(max_digits=15, decimal_places=5, blank=True, null=True)
    weight = models.DecimalField(max_digits=15, decimal_places=5, blank=True, null=True)
    value_date = models.DateField()

class Breakdown(models.Model):
    fund = models.ForeignKey(Fund)
    category = models.ForeignKey(Category)
    mtd = models.DecimalField(max_digits=15, decimal_places=5, blank=True, null=True)
    ytd = models.DecimalField(max_digits=15, decimal_places=5, blank=True, null=True)
    base_nav = models.DecimalField(max_digits=15, decimal_places=5, blank=True, null=True)
    euro_nav = models.DecimalField(max_digits=15, decimal_places=5, blank=True, null=True)
    weight = models.DecimalField(max_digits=15, decimal_places=5, blank=True, null=True)
    cash_flow_euro_amount_euro_dollar = models.DecimalField(max_digits=15, decimal_places=5, blank=True, null=True)
    cash_flow_percent_euro_dollar = models.DecimalField(max_digits=15, decimal_places=5, blank=True, null=True)
    #net_movement = models.DecimalField(max_digits=15, decimal_places=5, blank=True, null=True)
    value_date = models.DateField()


