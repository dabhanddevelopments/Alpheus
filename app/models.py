from django.db import models
from django.contrib.auth.models import User, Group
from mptt.models import MPTTModel, TreeForeignKey

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
    size_y = models.SmallIntegerField()
    size_x = models.SmallIntegerField()
    column_width = models.SmallIntegerField(blank=True, null=True,
                                help_text="Only applicable for data grids")
    position = models.PositiveSmallIntegerField("Position")

    class Meta:
        ordering = ['position']

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


class Fund(models.Model):
    
    fund_type = models.ForeignKey(FundType, related_name="fund")
    counter_party = models.ForeignKey('CounterParty')
    alarm = models.ForeignKey('Alarm', blank=True, null=True)
    benchmark = models.ForeignKey('Benchmark', blank=True, null=True)
    name = models.CharField(max_length=200, null=True)
    aum = models.SmallIntegerField()
    mtd = models.SmallIntegerField()
    ytd = models.SmallIntegerField()
    one_day_var = models.SmallIntegerField()
    total_cash = models.SmallIntegerField(verbose_name="Total Cash Held in Fund")
    usd_hedge = models.SmallIntegerField(verbose_name="USD Positions Current FX Hedge")
    checks = models.SmallIntegerField()
    unsettled = models.SmallIntegerField()
   
    def __unicode__(self):
        return self.name

class FundBench(models.Model):
    name = models.CharField(max_length=50)
    funds = models.ManyToManyField(Fund)


class FundBenchHist(models.Model):
    benchmark = models.ForeignKey(FundBench)
    value_date = models.DateField()
    value = models.DecimalField(max_digits=20, decimal_places=2)
    ann_return = models.DecimalField(max_digits=4, decimal_places=2)
    ann_volatility = models.DecimalField(max_digits=4, decimal_places=2)
    sharpe_ratio = models.DecimalField(max_digits=4, decimal_places=2)
    


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
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    alarm = models.ForeignKey('Alarm', blank=True, null=True)
    benchmark = models.ForeignKey('Benchmark', blank=True, null=True)

    def __unicode__(self):
        return u'%s / %s' % (self.first_name, self.last_name)

class HistoricClient(models.Model):
    client = models.ForeignKey(Client)

class Currency(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=3)

class Country(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=3)


# deposit, withdrawal, buy sell stocks etc
class TradeType(models.Model):
    pass

# Trade does not have a history table
class Trade(models.Model):
    holding = models.ForeignKey('Holding')
    identifier = models.IntegerField()
    trade_type = models.ForeignKey(TradeType)
    trade_date = models.DateField()
    settlement_date = models.DateField()
    purchase_sale = models.BooleanField()
    no_of_units = models.DecimalField(max_digits=20, decimal_places=2,\
                                                verbose_name="No. of Units")
    purchase_price = models.DecimalField(max_digits=20, decimal_places=5)
    currency = models.ForeignKey(Currency)
    fx_euro = models.DecimalField(max_digits=20, decimal_places=8,\
                                                verbose_name="FX to Euro")
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
HOLDING_GROUP = (
    (GROUP_ALL, 'All'),
    (GROUP_SEC, 'Sector'),
    (GROUP_SUB, 'Sub-Sector'),
    (GROUP_LOC, 'Location'),
    (GROUP_ASS, 'Asset Class'),
)
class Holding(models.Model):
     #name = models.CharField(max_length=50)

    #class HoldingHistorical(models.Model):
    name = models.CharField(max_length=50)
    identifier = models.IntegerField()
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
    nav = models.DecimalField(max_digits=20, decimal_places=2,\
                                                verbose_name="NAV")
    holding_group = models.CharField(max_length=3,
                                choices=HOLDING_GROUP,
                                default=GROUP_ALL)
    description = models.TextField()
    value_date = models.DateField()
    rep_code = models.CharField(max_length=50)
    isin = models.CharField(max_length=12)
    valoren = models.IntegerField()
    interest_rate = models.DecimalField(max_digits=20, decimal_places=5)
    weight = models.DecimalField(max_digits=20, decimal_places=5)
    current_price = models.DecimalField(max_digits=20, decimal_places=8)
    no_of_units = models.DecimalField(max_digits=20, decimal_places=2,\
                                                verbose_name="No. of Units")

      
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

class HoldPerfYearly(models.Model):
    #holding = models.ForeignKey(Holding)
    fund = models.ForeignKey(Fund)
    holding_group = models.CharField(max_length=3,
                                choices=HOLDING_GROUP,
                                default=GROUP_ALL)
    holding_category = models.ForeignKey(HoldingCategory)
    si = models.DecimalField(max_digits=4, decimal_places=2)
    ytd = models.DecimalField(max_digits=4, decimal_places=2)
    year = models.SmallIntegerField()

    def __unicode__(self):
        return "%s - %s - %s" % (self.holding.name, \
                    self.fund.name, self.year)

    class Meta:
            ordering = ['year']

class HoldPerfMonthly(models.Model):
    #holding = models.ForeignKey(Holding)
    fund = models.ForeignKey(Fund)
    holding_group = models.CharField(max_length=3,
                                choices=HOLDING_GROUP,
                                default=GROUP_ALL)
    holding_category = models.ForeignKey(HoldingCategory)
    #yearly = models.ForeignKey(HoldPerfYearly)
    value = models.DecimalField(max_digits=4, decimal_places=2)
    year = models.SmallIntegerField()
    month = models.SmallIntegerField()

    #class Meta:
    #    unique_together = (('holding_group', 'year'), ('year', 'month'))

    def __unicode__(self):
        return self.name

class FundPerfDaily(models.Model):
    fund = models.ForeignKey(Fund)
    holding = models.ForeignKey(Holding, null=True, blank=True)
    value = models.DecimalField(max_digits=4, decimal_places=2)
    date = models.DateField()

    def __unicode__(self):
        return str(self.value)


class FundPerfMonthly(models.Model):
    fund = models.ForeignKey(Fund)
    holding_group = models.CharField(max_length=3,
                                choices=HOLDING_GROUP,
                                default=GROUP_ALL)
    holding_category = models.ForeignKey(HoldingCategory,
                related_name='category', null=True, blank=True)
    value = models.DecimalField(max_digits=4, decimal_places=2)
    ann_return = models.DecimalField(max_digits=4, decimal_places=2)
    ann_volatility = models.DecimalField(max_digits=4, decimal_places=2)
    sharpe_ratio = models.DecimalField(max_digits=4, decimal_places=2)
    year = models.SmallIntegerField()
    month = models.SmallIntegerField()
    value_date = models.DateField()

    class Meta:
        #unique_together = ('holding_group', 'holding_category',)
        pass

    def __unicode__(self):
        return self.fund.name

class FundPerfYearly(models.Model):
    fund = models.ForeignKey(Fund)
    holding_group = models.CharField(max_length=3,
                                choices=HOLDING_GROUP,
                                default=GROUP_ALL)
    holding_category = models.ForeignKey(HoldingCategory,
                                        null=True, blank=True)
    year = models.SmallIntegerField()
    ytd = models.DecimalField(max_digits=15, decimal_places=5)
    si = models.DecimalField(max_digits=15, decimal_places=5)

    def __unicode__(self):
        return self.fund.name

    class Meta:
        #unique_together = ('holding_group', 'holding_category',)
        ordering = ['year']



class Alarm(models.Model):
    pass

class Benchmark(models.Model):
    pass


