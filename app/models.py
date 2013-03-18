from django.db import models
from django.contrib.auth.models import User, Group
from mptt.models import MPTTModel, TreeForeignKey



# Widget types are table, chart, graph etc
class WidgetType(models.Model):
    key = models.CharField(max_length=50)
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name


class Widget(models.Model):
    name = models.CharField(max_length=50)
    key = models.CharField(max_length=50)
    widget_type = models.ForeignKey(WidgetType)
    access = models.ManyToManyField(Group)
    size_y = models.SmallIntegerField()
    size_x = models.SmallIntegerField()
    description = models.TextField()

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


class PageWidget(models.Model):

    # If the user is zero it is the default configuration
    user = models.ForeignKey(User, null=True)
    page = models.ForeignKey(Page)
    widget = models.ForeignKey(Widget)

    size_y = models.SmallIntegerField()
    size_x = models.SmallIntegerField()
    col    = models.SmallIntegerField()
    row    = models.SmallIntegerField()

    class Meta:
        verbose_name = "Widget on Page"
        verbose_name_plural = "Widgets on Page"

    def __unicode__(self):
        return u'%s / %s' % (self.page.title, self.widget.name)

APPEND_LIST = (
    ('fund', 'Fund List'),
    ('client', 'Client List'),
)
class Menu(MPTTModel):
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    page = models.ForeignKey(Page, blank=True, null=True)
    name = models.CharField(max_length=50)
    access = models.ManyToManyField(Group)

    def __unicode__(self):
        try:
            self.parent.name
            return u'%s / %s' % (self.parent.name, self.name)
        except:
            return self.name


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
    trade_type = models.ForeignKey(TradeType)

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

class Holding(models.Model):
    name = models.CharField(max_length=50)
    fee = models.ForeignKey(Fee)
    fund = models.ForeignKey(Fund)
    description = models.TextField()
    nav_date = models.DateTimeField()
    rep_code = models.CharField(max_length=50)
    currency = models.ForeignKey(Currency)
    isin = models.CharField(max_length=12)
    valoren = models.IntegerField()
    interest_rate = models.DecimalField(max_digits=20, decimal_places=5)
    country = models.ForeignKey(Country)
    counter_party = models.ForeignKey('CounterParty')

class HoldingType(models.Model):
    name = models.CharField(max_length=50)
    key = models.CharField(max_length=50)

class HistoricalHolding(models.Model):
    holding = models.ForeignKey(Holding)

class Alarm(models.Model):
    pass

class Benchmark(models.Model):
    pass

