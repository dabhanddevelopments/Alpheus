from django.db import models
from django.contrib.auth.models import User, Group
from mptt.models import MPTTModel, TreeForeignKey

YES_NO=(
    (1,'Yes'),
    (2,'No'),
)
SUBSCRIPTION_FREQUENCY=(
    (1,'D'),
    (2,'M'),
    (3,'Q'),
    (4,'SA'),
    (5,'A'),
)

FREQUENCY=(
    (1,'M'),
    (2,'Q'),
    (3,'SA'),
    (4,'A'),
)
SUBSCRIPTION_REDEMPTION=(
    (1,'Subscription'),
    (2,'Redemption'),
)
BUY_SELL=(
    (1,'Buy'),
    (2,'Sell'),
)
PERCENT_RELEASED=(
    (90,'90%'),
    (100,'100%'),
)


class Window(models.Model):

    WINDOW_LAYOUT = (
        ('v', 'Vertical'),
        ('h', 'Horizontal')
    )
    name = models.CharField(max_length=50)
    key = models.CharField(max_length=50)
    access = models.ManyToManyField(Group)
    size_y = models.SmallIntegerField()
    size_x = models.SmallIntegerField()
    layout = models.CharField(max_length=1, choices=WINDOW_LAYOUT,
            help_text="Layout for multiple widgets on window.")

    def __unicode__(self):
        return self.name


# Widget types are table, chart, graph etc
class WidgetType(models.Model):
    key = models.CharField(max_length=50)
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name

class WidgetParam(models.Model):
    key = models.CharField(max_length=50)
    value = models.CharField(max_length=50)

    def __unicode__(self):
        return '%s=%s' % (self.key, self.value)

class Widget(models.Model):
    name = models.CharField(max_length=50)
    key = models.CharField(max_length=50)
    widget_type = models.ForeignKey(WidgetType)
    widget_param = models.ManyToManyField(WidgetParam, null=True, blank=True)
    window = models.ForeignKey(Window)
    description = models.TextField(blank=True, null=True)
    size_y = models.DecimalField(max_digits=3, decimal_places=1)
    size_x = models.DecimalField(max_digits=3, decimal_places=1)
    column_width = models.SmallIntegerField(blank=True, null=True,
                                help_text="Only applicable for data grids")
    position = models.PositiveSmallIntegerField("Position")

    class Meta:
        ordering = ['position', 'name']

    def __unicode__(self):
        return self.name


# If the page has a parent, it is part of a tab panel
class Page(MPTTModel):
    parent = models.ForeignKey('self', blank=True, null=True,
                              related_name='children')
    title = models.CharField(max_length=50)

    def __unicode__(self):
        try:
            self.parent.title
            return u'%s / %s' % (self.parent.title, self.title)
        except:
            return self.title

class PageWindow(models.Model):

    # If the user is zero it is the default configuration
    user = models.ForeignKey(User, null=True)
    page = models.ForeignKey(Page)
    window = models.ForeignKey(Window)
    size_y = models.SmallIntegerField()
    size_x = models.SmallIntegerField()
    col    = models.SmallIntegerField()
    row    = models.SmallIntegerField()

    class Meta:
        verbose_name = "Window on page"
        verbose_name_plural = "Windows on page"

    def __unicode__(self):
        return u'%s / %s' % (self.page.title, self.window.name)


class FundType(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name

class Classification(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name
        
class Custodian(models.Model):
    name = models.CharField(max_length=50)
    contact_name = models.CharField(max_length=50)
    contact_number = models.CharField(max_length=50)
    performance_fee =  models.DecimalField(max_digits=15, decimal_places=5)
    management_fee =  models.DecimalField(max_digits=15, decimal_places=5)

    def __unicode__(self):
        return self.name
        
class Auditor(models.Model):
    name = models.CharField(max_length=50)
    contact_name = models.CharField(max_length=50)
    contact_number = models.CharField(max_length=50)
    fee =  models.DecimalField(max_digits=15, decimal_places=5)

    def __unicode__(self):
        return self.name

class Administrator(models.Model):
    name = models.CharField(max_length=50)
    contact_name = models.CharField(max_length=50)
    contact_number = models.CharField(max_length=50)
    fee =  models.DecimalField(max_digits=15, decimal_places=5)
    
    def __unicode__(self):
        return self.name

class CurrencyPositionMonth(models.Model):
    fund = models.ForeignKey('Fund')
    currency = models.ForeignKey('Currency')
    nav = models.DecimalField(max_digits=20, decimal_places=5,\
                                             verbose_name="NAV")
    value_date = models.DateField()

class FxRate(models.Model):
    value_date = models.DateField()
    currency = models.ForeignKey('Currency')
    fx_rate = models.DecimalField(max_digits=15, decimal_places=5)
    
class FxHedge(models.Model):
    fund = models.ForeignKey('Fund')
    trade_date = models.DateField()
    settlement_date = models.DateField()
    buy_sell = models.SmallIntegerField(choices=BUY_SELL)
    currency = models.ForeignKey('Currency')
    amount = models.DecimalField(max_digits=20, decimal_places=5)
  

class Fund(models.Model):

    fund_type = models.ForeignKey(FundType, related_name="fund_type")
    counter_party = models.ForeignKey('CounterParty')
    alarm = models.ForeignKey('Alarm', blank=True, null=True)
    benchmark = models.ForeignKey('FundBench', blank=True, null=True)
    custodian = models.ForeignKey('Custodian')
    auditor = models.ForeignKey('Auditor')
    administrator =  models.ForeignKey('Administrator')
    classification = models.ForeignKey(Classification, related_name="fund_class")
    manager = models.ForeignKey(User)
    name = models.CharField(max_length=200, null=True)
    aum = models.DecimalField(max_digits=20, decimal_places=5)
    mtd = models.DecimalField(max_digits=20, decimal_places=5)
    ytd = models.DecimalField(max_digits=20, decimal_places=5)
    description = models.CharField(max_length=2000, null=True, blank=True)
    subscription_frequency = models.SmallIntegerField(choices=FREQUENCY)
    redemption_frequency = models.SmallIntegerField(choices=FREQUENCY)
    performance_fee =  models.DecimalField(max_digits=15, decimal_places=5)
    management_fee =  models.DecimalField(max_digits=15, decimal_places=5)
    #one_day_var = models.SmallIntegerField()
    #total_cash = models.SmallIntegerField(verbose_name="Total Cash Held in Fund")
    #usd_hedge = models.SmallIntegerField(verbose_name="USD Positions Current FX Hedge")
    #checks = models.SmallIntegerField()
    #unsettled = models.SmallIntegerField()



    def __unicode__(self):
        return self.name

class FundBench(models.Model):
    name = models.CharField(max_length=50)
    funds = models.ManyToManyField(Fund)

    # instead of looking for the latest value in the historical table
    mtd = models.DecimalField(max_digits=15, decimal_places=5) # formerly known as performance


class FundBenchHist(models.Model):
    benchmark = models.ForeignKey(FundBench)
    value_date = models.DateField()
    performance = models.DecimalField(max_digits=15, decimal_places=5)
    net_drawdown = models.DecimalField(max_digits=15, decimal_places=5)
    si = models.DecimalField(max_digits=15, decimal_places=5)
    ann_return1 = models.DecimalField(max_digits=4, decimal_places=2)
    ann_return3 = models.DecimalField(max_digits=4, decimal_places=2)
    ann_return5 = models.DecimalField(max_digits=4, decimal_places=2)
    ann_volatility1 = models.DecimalField(max_digits=4, decimal_places=2)
    ann_volatility3 = models.DecimalField(max_digits=4, decimal_places=2)
    ann_volatility5 = models.DecimalField(max_digits=4, decimal_places=2)
    sharpe_ratio1 = models.DecimalField(max_digits=4, decimal_places=2)
    sharpe_ratio3 = models.DecimalField(max_digits=4, decimal_places=2)
    sharpe_ratio5 = models.DecimalField(max_digits=4, decimal_places=2)
    alpha1 = models.DecimalField(max_digits=4, decimal_places=2)
    alpha3 = models.DecimalField(max_digits=4, decimal_places=2)
    alpha5 = models.DecimalField(max_digits=4, decimal_places=2)
    beta1 = models.DecimalField(max_digits=4, decimal_places=2)
    beta3 = models.DecimalField(max_digits=4, decimal_places=2)
    beta5 = models.DecimalField(max_digits=4, decimal_places=2)
    correlation1 = models.DecimalField(max_digits=4, decimal_places=2)
    correlation3 = models.DecimalField(max_digits=4, decimal_places=2)
    correlation5 = models.DecimalField(max_digits=4, decimal_places=2)


class Menu(MPTTModel):
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    page = models.ForeignKey(Page, blank=True, null=True)
    fund = models.ForeignKey(Fund, blank=True, null=True)
    name = models.CharField(max_length=50)
    access = models.ManyToManyField(Group)

    def __unicode__(self):
        try:
            self.parent.name
            return u'%s / %s' % (self.parent.name, self.name)
        except:
            return self.name



class HistoricFund(models.Model):
    fund = models.ForeignKey(Fund)


class Client(models.Model):
    alarm = models.ForeignKey('Alarm', blank=True, null=True)
    benchmark = models.ForeignKey('Benchmark', blank=True, null=True)   
   
    fund = models.ManyToManyField(Fund, through="SubscriptionRedemption")
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    pending_nav = models.DecimalField(max_digits=20, decimal_places=2)
    nav = models.DecimalField(max_digits=20, decimal_places=2)
    no_of_units = models.DecimalField(max_digits=20, decimal_places=2,\
                                                verbose_name="No. of Units")
                                             
    
    def __unicode__(self):
        return u'%s / %s' % (self.first_name, self.last_name)

class HistoricClient(models.Model):
    client = models.ForeignKey(Client)

class Currency(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=3)
    def __unicode__(self):
        return self.name
        
class Country(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=3)


# deposit, withdrawal, buy sell stocks etc
class TradeType(models.Model):
    pass

class PurchaseSale(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name


# Trade does not have a history table

class Trade(models.Model):
    holding = models.ForeignKey('Holding')
    identifier = models.IntegerField()
    trade_type = models.ForeignKey(TradeType)
    trade_date = models.DateField()
    settlement_date = models.DateField()
    purchase_sale = models.ForeignKey(PurchaseSale) #to be deleted same as buy sell
    buy_sell = models.SmallIntegerField(choices=BUY_SELL)
    no_of_units = models.DecimalField(max_digits=20, decimal_places=2,\
                                                verbose_name="No. of Units")
    purchase_price = models.DecimalField(max_digits=20, decimal_places=5)
    purchase_price_base = models.DecimalField(max_digits=20, decimal_places=5)
    nav_purchase = models.DecimalField(max_digits=20, decimal_places=5)
    currency = models.ForeignKey(Currency)
    fx_euro = models.DecimalField(max_digits=20, decimal_places=8,\
                                                verbose_name="FX to Euro")
    # not used to be deleted
    dealing_date = models.DateField()
    # purchase_price_euro = models.DecimalField(max_digits=20, decimal_places=5)

class Fee(models.Model):
    pass

class HistoricalFee(models.Model):
    fee = models.ForeignKey(Fee)

# company expenses, salary etc
class Expense(models.Model):
    pass

# why?
class HistoricalExpense(models.Model):
    expense = models.ForeignKey(Expense)

# The person taking your trade order
class CounterParty(models.Model):
    name = models.CharField(max_length=50)


GROUP_ALL = 'all'
GROUP_SEC = 'sec'
GROUP_SUB = 'sub'
GROUP_LOC = 'loc'
GROUP_ASS = 'ass'
GROUP_CUR = 'cur'
HOLDING_GROUP = (
    (GROUP_ALL, 'All'),
    (GROUP_SEC, 'Sector'),
    (GROUP_SUB, 'Sub-Sector'),
    (GROUP_LOC, 'Location'),
    (GROUP_ASS, 'Asset Class'),
    (GROUP_CUR, 'Currency'),
)
class Holding(models.Model):
    name = models.CharField(max_length=50)
    fee = models.ForeignKey(Fee, blank=True, null=True)
    fund = models.ForeignKey(Fund)
    currency = models.ForeignKey(Currency)
    country = models.ForeignKey(Country)
    counter_party = models.ForeignKey('CounterParty')
    sector = models.ForeignKey('HoldingCategory', related_name='sector')
    sub_sector = models.ForeignKey('HoldingCategory', related_name='sub_sector')
    location = models.ForeignKey('HoldingCategory', related_name='location')
    asset_class = models.ForeignKey('HoldingCategory',\
                                    related_name='asset_class')
    isin = models.CharField(max_length=12)
    rep_code = models.CharField(max_length=50)
    description = models.TextField()
    valoren = models.IntegerField()

    # fields recorded in the historical holding table HoldPerf
    # all of them might not be necessary to store here
    mtd = models.DecimalField(max_digits=15, decimal_places=5)
    nav = models.DecimalField(max_digits=20, decimal_places=2,\
                                             verbose_name="NAV")
    interest_rate = models.DecimalField(max_digits=20, decimal_places=5)


    current_price = models.DecimalField(max_digits=20, decimal_places=8)
    no_of_units = models.DecimalField(max_digits=20, decimal_places=2,\
                                                verbose_name="No. of Units")
    price_of_unit = models.DecimalField(max_digits=20, decimal_places=5)
    weight = models.DecimalField(max_digits=20, decimal_places=5)
    cumulative_nav = models.DecimalField(max_digits=20, decimal_places=5)
    cumulative_weight = models.DecimalField(max_digits=20, decimal_places=5)
    value_date = models.DateField()

    # static trade data
    dealing_date = models.DateField()
    redemption_frequency = models.SmallIntegerField(choices=FREQUENCY)
    redemption_date = models.DateField()
    redemption_notice = models.DecimalField(max_digits=20, decimal_places=5)
    max_redemption = models.DecimalField(max_digits=20, decimal_places=5)
    payment_days = models.DecimalField(max_digits=20, decimal_places=5)
    gate = models.DecimalField(max_digits=20, decimal_places=5)
    soft_lock = models.SmallIntegerField(choices=YES_NO)
    redemption_fee12 = models.DecimalField(max_digits=20, decimal_places=5,\
                                                verbose_name="Redemption Fee 12M")
    redemption_fee24 = models.DecimalField(max_digits=20, decimal_places=5,\
                                                verbose_name="Redemption Fee 24M")
    redemption_fee36 = models.DecimalField(max_digits=20, decimal_places=5,\
                                                verbose_name="Redemption Fee 36M")
    
    def soft_lock2(self):
        return self.get_soft_lock_display()
    
    def __unicode__(self):
        return str(self.id)

    class Meta:
            ordering = ["id"]

class HoldingCategory(models.Model):
    name = models.CharField(max_length=50)
    holding_group = models.CharField(max_length=3,
                                choices=HOLDING_GROUP,
                                default=GROUP_ALL)

    def __unicode__(self):
        return self.name


class HoldingType(models.Model):
    name = models.CharField(max_length=50)
    key = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name

class HoldPerfMonth(models.Model):
    fund = models.ForeignKey(Fund)
    holding = models.ForeignKey(Holding)
    holding_category = models.ForeignKey(HoldingCategory, null=True, blank=True)
    si = models.DecimalField(max_digits=4, decimal_places=2)
    ytd = models.DecimalField(max_digits=4, decimal_places=2)
    performance = models.DecimalField(max_digits=4, decimal_places=2)
    nav = models.DecimalField(max_digits=20, decimal_places=5,\
                                             verbose_name="NAV")
    weight = models.DecimalField(max_digits=20, decimal_places=5)
    value_date = models.DateField()

    #class Meta:
    #    unique_together = (('holding_group', 'year'), ('year', 'month'))

    def __unicode__(self):
        return str(self.value_date)

# @TODO: Consider renaming this model HoldingHistory
class HoldPerf(models.Model):
    holding = models.ForeignKey(Holding)
    holding_category = models.ForeignKey(HoldingCategory)
    month = models.ForeignKey(HoldPerfMonth)
    nav = models.DecimalField(max_digits=20, decimal_places=2,\
                                             verbose_name="NAV")
    # not used?
    interest_rate = models.DecimalField(max_digits=20, decimal_places=5)

    # equivalent to value in fund performance
    performance = models.DecimalField(max_digits=20, decimal_places=5)

    #
    current_price = models.DecimalField(max_digits=20, decimal_places=8)
    no_of_units = models.DecimalField(max_digits=20, decimal_places=2,\
                                                verbose_name="No. of Units")
    weight = models.DecimalField(max_digits=20, decimal_places=5)
    value_date = models.DateField()


# FUND PERFORMANCE

class FundPerfYear(models.Model):
    fund = models.ForeignKey(Fund, related_name='fund')
    ytd = models.DecimalField(max_digits=15, decimal_places=5)
    si = models.DecimalField(max_digits=15, decimal_places=5)
    value_date = models.DateField()


class FundPerfMonth(models.Model):
    fund = models.ForeignKey(Fund)
    year = models.ForeignKey(FundPerfYear, related_name='month')
    performance = models.DecimalField(max_digits=4, decimal_places=2)
    net_drawdown = models.DecimalField(max_digits=15, decimal_places=5)
    ytd = models.DecimalField(max_digits=15, decimal_places=5)
    si = models.DecimalField(max_digits=15, decimal_places=5)
    ann_return1 = models.DecimalField(max_digits=4, decimal_places=2)
    ann_return3 = models.DecimalField(max_digits=4, decimal_places=2)
    ann_return5 = models.DecimalField(max_digits=4, decimal_places=2)
    ann_volatility1 = models.DecimalField(max_digits=4, decimal_places=2)
    ann_volatility3 = models.DecimalField(max_digits=4, decimal_places=2)
    ann_volatility5 = models.DecimalField(max_digits=4, decimal_places=2)
    sharpe_ratio1 = models.DecimalField(max_digits=4, decimal_places=2)
    sharpe_ratio3 = models.DecimalField(max_digits=4, decimal_places=2)
    sharpe_ratio5 = models.DecimalField(max_digits=4, decimal_places=2)
    alpha1 = models.DecimalField(max_digits=4, decimal_places=2)
    alpha3 = models.DecimalField(max_digits=4, decimal_places=2)
    alpha5 = models.DecimalField(max_digits=4, decimal_places=2)
    beta1 = models.DecimalField(max_digits=4, decimal_places=2)
    beta3 = models.DecimalField(max_digits=4, decimal_places=2)
    beta5 = models.DecimalField(max_digits=4, decimal_places=2)
    correlation1 = models.DecimalField(max_digits=4, decimal_places=2)
    correlation3 = models.DecimalField(max_digits=4, decimal_places=2)
    correlation5 = models.DecimalField(max_digits=4, decimal_places=2)
    no_of_units = models.DecimalField(max_digits=20, decimal_places=5)
    euro_nav = models.DecimalField(max_digits=20, decimal_places=5)
    no_of_units_fund = models.DecimalField(max_digits=20, decimal_places=5)
    euro_nav_fund = models.DecimalField(max_digits=20, decimal_places=5)
    value_date = models.DateField()
    
    previous_nav = models.DecimalField(max_digits=20, decimal_places=2) #last months nav, is this needed?
    performance_fees_added_back = models.DecimalField(max_digits=20, decimal_places=2)# not being imported by alexi? input form?
    subscription_amount = models.DecimalField(max_digits=20, decimal_places=2)
    redemption_amount = models.DecimalField(max_digits=20, decimal_places=2)
    net_movement = models.DecimalField(max_digits=20, decimal_places=2)
    gross_assets_after_subs_red = models.DecimalField(max_digits=20, decimal_places=2)
    
    nav_securities = models.DecimalField(max_digits=20, decimal_places=2)
    nav_securities_total = models.DecimalField(max_digits=20, decimal_places=2)
    nav_cash = models.DecimalField(max_digits=20, decimal_places=2)
    nav_other_assets = models.DecimalField(max_digits=20, decimal_places=2)
    
    administration_fees = models.DecimalField(max_digits=20, decimal_places=2)
    audit_fees = models.DecimalField(max_digits=20, decimal_places=2)
    capital_payable = models.DecimalField(max_digits=20, decimal_places=2)
    corporate_secretarial_fees = models.DecimalField(max_digits=20, decimal_places=2)
    custodian_fees = models.DecimalField(max_digits=20, decimal_places=2)
    financial_statement_prep_fees = models.DecimalField(max_digits=20, decimal_places=2)
    sub_advisory_fees = models.DecimalField(max_digits=20, decimal_places=2)
    management_fees = models.DecimalField(max_digits=20, decimal_places=2)
    performance_fees = models.DecimalField(max_digits=20, decimal_places=2)
    other_liabilities = models.DecimalField(max_digits=20, decimal_places=2)
    total_liabilities = models.DecimalField(max_digits=20, decimal_places=2)
    

    class Meta:
        #unique_together = ('holding_group', 'holding_category',)
        ordering = ['value_date']

    #def __unicode__(self):
    #    return str(self.value_date)


class FundPerf(models.Model):
    fund = models.ForeignKey(Fund)
    month = models.ForeignKey(FundPerfMonth)
    performance = models.DecimalField(max_digits=4, decimal_places=2)
    value_date = models.DateField()

    def __unicode__(self):
        return str(self.performance)



class Alarm(models.Model):
    name = models.CharField(max_length=50)

class Benchmark(models.Model):
    pass




class SubscriptionRedemption(models.Model):
    fund = models.ForeignKey(Fund)
    client = models.ForeignKey(Client)
    trade_date = models.DateField()
    input_date = models.DateField()
    no_of_units = models.DecimalField(max_digits=20, decimal_places=5)
    sub_red = models.SmallIntegerField(choices=SUBSCRIPTION_REDEMPTION)
    nav = models.DecimalField(max_digits=20, decimal_places=5)
    percent_released = models.SmallIntegerField(choices=PERCENT_RELEASED)
    
    
#Client Historic


class ClientPerfMonth(models.Model):
    # consider making these two generic
    fund = models.ForeignKey(Fund, related_name='fund_month', null=True, blank=True)
    holding = models.ForeignKey(Holding, related_name='hold_month', null=True, blank=True)
    
    client = models.ForeignKey(Client, related_name='client_month')
    performance = models.DecimalField(max_digits=4, decimal_places=2)
    net_drawdown = models.DecimalField(max_digits=15, decimal_places=5)
    ytd = models.DecimalField(max_digits=15, decimal_places=5)
    si = models.DecimalField(max_digits=15, decimal_places=5)
    ann_return1 = models.DecimalField(max_digits=4, decimal_places=2)
    ann_return3 = models.DecimalField(max_digits=4, decimal_places=2)
    ann_return5 = models.DecimalField(max_digits=4, decimal_places=2)
    ann_volatility1 = models.DecimalField(max_digits=4, decimal_places=2)
    ann_volatility3 = models.DecimalField(max_digits=4, decimal_places=2)
    ann_volatility5 = models.DecimalField(max_digits=4, decimal_places=2)
    sharpe_ratio1 = models.DecimalField(max_digits=4, decimal_places=2)
    sharpe_ratio3 = models.DecimalField(max_digits=4, decimal_places=2)
    sharpe_ratio5 = models.DecimalField(max_digits=4, decimal_places=2)
    alpha1 = models.DecimalField(max_digits=4, decimal_places=2)
    alpha3 = models.DecimalField(max_digits=4, decimal_places=2)
    alpha5 = models.DecimalField(max_digits=4, decimal_places=2)
    beta1 = models.DecimalField(max_digits=4, decimal_places=2)
    beta3 = models.DecimalField(max_digits=4, decimal_places=2)
    beta5 = models.DecimalField(max_digits=4, decimal_places=2)
    correlation1 = models.DecimalField(max_digits=4, decimal_places=2)
    correlation3 = models.DecimalField(max_digits=4, decimal_places=2)
    correlation5 = models.DecimalField(max_digits=4, decimal_places=2)

    euro_nav = models.DecimalField(max_digits=20, decimal_places=2)
    value_date = models.DateField()
    previous_nav = models.DecimalField(max_digits=20, decimal_places=2) #last months nav, is this needed?
    performance_fees_added_back = models.DecimalField(max_digits=20, decimal_places=2)# not being imported by alexi? input form?
    subscription_amount = models.DecimalField(max_digits=20, decimal_places=2)
    redemption_amount = models.DecimalField(max_digits=20, decimal_places=2)
    net_movement = models.DecimalField(max_digits=20, decimal_places=2)
    gross_assets_after_subs_red = models.DecimalField(max_digits=20, decimal_places=2)
    pending_nav = models.DecimalField(max_digits=20, decimal_places=2)
    nav = models.DecimalField(max_digits=20, decimal_places=2)
    no_of_units = models.DecimalField(max_digits=20, decimal_places=2,\
                                                verbose_name="No. of Units")
    
    
    class Meta:
        #unique_together = ('holding_group', 'holding_category',)
        ordering = ['value_date']

    
    
