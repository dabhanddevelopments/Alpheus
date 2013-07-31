from django.db import models
from fund.models import Fund, CounterParty
from client.models import Client
from app.models import ModelBase, DATE_TYPE, FREQUENCY, YES_NO, Currency, Country, Fee


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

    performance = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    ytd = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    si = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    weight = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    #weight_of_trades #W76 - liquidity adjusted to confirm
    error_range = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    cash_flow = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    nav = models.DecimalField(max_digits=20, decimal_places=5,blank=True, null=True, verbose_name="NAV")
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
    delta_valuation = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    delta_flow = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    cash_flow = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    fx_rate = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    net_movement = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
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
    dealing_date = models.DateField()
    value_date = models.DateField()

class Holding(HoldingBase):
    fund = models.ManyToManyField(Fund)
    client = models.ManyToManyField(Client, related_name="holding_client")
    currency = models.ForeignKey(Currency, related_name='holding_currency')
    country = models.ForeignKey(Country, related_name='holding_country')
    fee = models.ForeignKey(Fee, blank=True, null=True, related_name='holding_fee')
    counter_party = models.ForeignKey(CounterParty, related_name='holding_counter_party')
    sector = models.ForeignKey(Category, related_name='sector')
    sub_sector = models.ForeignKey(Category, related_name='sub_sector')
    location = models.ForeignKey(Category, related_name='location')
    investment_type = models.ForeignKey(Category, related_name='investment_type')
    asset_class = models.ForeignKey(Category, related_name='asset_class')
    name = models.CharField(max_length=50)
    isin = models.CharField(max_length=12)
    rep_code = models.CharField(max_length=50)
    description = models.TextField()
    valoren = models.IntegerField()

    redemption_frequency = models.SmallIntegerField(choices=FREQUENCY)
    redemption_date = models.DateField()
    redemption_notice = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    max_redemption = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    payment_days = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    gate = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    soft_lock = models.SmallIntegerField(choices=YES_NO, blank=True, null=True)
    redemption_fee12 = models.DecimalField(max_digits=20, decimal_places=5,\
                                                blank=True, null=True, verbose_name="Redemption Fee 12M")
    redemption_fee24 = models.DecimalField(max_digits=20, decimal_places=5,\
                                                blank=True, null=True, verbose_name="Redemption Fee 24M")
    redemption_fee36 = models.DecimalField(max_digits=20, decimal_places=5,\

                                               blank=True, null=True, verbose_name="Redemption Fee 36M")

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
    si = models.DecimalField(max_digits=15, decimal_places=5, blank=True, null=True)
    nav = models.DecimalField(max_digits=15, decimal_places=5, blank=True, null=True)
    weight = models.DecimalField(max_digits=15, decimal_places=5, blank=True, null=True)
    value_date = models.DateField()

class Breakdown(models.Model):
    fund = models.ForeignKey(Fund)
    category = models.ForeignKey(Category)
    mtd = models.DecimalField(max_digits=15, decimal_places=5, blank=True, null=True)
    ytd = models.DecimalField(max_digits=15, decimal_places=5, blank=True, null=True)
    si = models.DecimalField(max_digits=15, decimal_places=5, blank=True, null=True)
    nav = models.DecimalField(max_digits=15, decimal_places=5, blank=True, null=True)
    weight = models.DecimalField(max_digits=15, decimal_places=5, blank=True, null=True)
    cash_flow_value = models.DecimalField(max_digits=15, decimal_places=5, blank=True, null=True)
    cash_flow_percent = models.DecimalField(max_digits=15, decimal_places=5, blank=True, null=True)
    net_movement = models.DecimalField(max_digits=15, decimal_places=5, blank=True, null=True)
    value_date = models.DateField()

class Trade(models.Model):
    holding = models.ForeignKey(Holding)
    fund = models.ForeignKey(Fund, blank=True, null=True)
    client = models.ForeignKey(Client, blank=True, null=True)
    currency = models.ForeignKey(Currency, related_name='trade_currency')
    #identifier = models.IntegerField()
    #trade_type = models.ForeignKey(TradeType)
    #purchase_sale = models.ForeignKey(PurchaseSale)
    no_of_units = models.DecimalField(max_digits=20, decimal_places=5,\
                                                blank=True, null=True, verbose_name="No. of Units")
    purchase_price = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    purchase_price_base = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    nav_purchase = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    fx_euro = models.DecimalField(max_digits=20, decimal_places=8,\
                                                blank=True, null=True, verbose_name="FX to Euro")

    drawdown = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    various = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    distribution = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    inflow_euro = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    inflow_dollar = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    outflow_euro = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    outflow_dollar = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)

    # purchase_price_euro = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    trade_date = models.DateField()
    settlement_date = models.DateField()




