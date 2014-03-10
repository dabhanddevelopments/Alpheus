from django.db import models
from django.contrib.auth.models import User, Group
from mptt.models import MPTTModel, TreeForeignKey

DATE_TYPE = (
    ('d', 'Day'),
    ('w', 'Week'),
    ('m', 'Month'),
)

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

"""
class PerformanceEstimate(models.Model):
    holding = models.ForeignKey('holding.Holding', null=True)
    fund = models.ForeignKey('fund.Fund', null=True)
    benchmark = models.ForeignKey('comparative.Benchmark', null=True)
    peer = models.ForeignKey('comparative.Peer', null=True)
    user = models.ForeignKey(User, verbose_name="Manager", null=True)
    value_date = models.DateField(null=True)
    estimated_mtd = models.DecimalField(null=True,max_digits=20, decimal_places=5)

    class Meta:
        db_table = 'fund_performanceestimate' #delete this

"""


class MonthlyManager(models.Manager):
    def get_query_set(self):
        return super(MonthlyManager, self).get_query_set().filter(date_type='m')

class DailyManager(models.Manager):
    def get_query_set(self):
        return super(MonthlyManager, self).get_query_set().filter(date_type='d')


class ModelBase(models.Model):
    class Meta:
        abstract = True

    objects = models.Manager()
    days = DailyManager()
    months = MonthlyManager()


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
        return '%s - %s' % (self.key, self.name)

    class Meta:
        ordering = ['key']

# Widget types are table, chart, graph etc
class WidgetType(models.Model):
    key = models.CharField(max_length=50)
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name

class WidgetParam(models.Model):
    key = models.CharField(max_length=50)
    value = models.CharField(max_length=200)

    def used_on_window(self):
        return ', '.join([widget.window.key for widget in self.widget_set.all()])

    class Meta:
        ordering = ['key']

    def __unicode__(self):
        return '%s=%s' % (self.key, self.value)

class Widget(models.Model):
    name = models.CharField(max_length=100)
    key = models.CharField(max_length=50)
    widget_type = models.ForeignKey(WidgetType, null=True, blank=True)
    widget_param = models.ManyToManyField(WidgetParam, null=True, blank=True)
    window = models.ForeignKey(Window)
    description = models.TextField(blank=True, null=True)
    size_y = models.DecimalField(max_digits=3, decimal_places=1)
    size_x = models.DecimalField(max_digits=3, decimal_places=1)
    column_width = models.CommaSeparatedIntegerField(blank=True, null=True,
                                                 max_length=50, help_text="""
            Width of data columns as comma seperated string:
            &lt;first column&gt;,&lt;other columns&gt;""")
    columns = models.CharField(blank=True, null=True,
                                                 max_length=300, help_text="""
            Columns as comma seperated string:
            &lt;first column&gt;,&lt;second column&gt;,&lt;third column&gt;""")
    position = models.PositiveSmallIntegerField("Position")
    v2 = models.BooleanField()
    disabled = models.BooleanField(default=False)

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
        try:
            return u'%s / %s' % (self.page.parent.title, self.window.name)
        except:
            return u'%s / %s' % (self.page.title, self.window.name)



class Menu(MPTTModel):
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    page = models.ForeignKey(Page, blank=True, null=True)
    fund = models.ForeignKey('v2.Fund', blank=True, null=True)
    name = models.CharField(max_length=50)
    access = models.ManyToManyField(Group)

    def __unicode__(self):
        try:
            self.parent.name
            return u'%s / %s' % (self.parent.name, self.name)
        except:
            return self.name


"""

class Classification(models.Model):
    key = models.CharField(max_length=50)
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name

class Custodian(models.Model):
    key = models.CharField(null=True,max_length=50)
    name = models.CharField(null=True,max_length=50)
    contact_name = models.CharField(null=True,max_length=50)
    contact_number = models.CharField(max_length=50, blank=True, null=True)
    performance_fee =  models.DecimalField(null=True,max_digits=15, decimal_places=5)
    management_fee =  models.DecimalField(null=True,max_digits=15, decimal_places=5)

    def __unicode__(self):
        return self.name

class Auditor(models.Model):
    name = models.CharField(null=True,max_length=50)
    contact_name = models.CharField(null=True,max_length=50)
    contact_number = models.CharField(max_length=50, blank=True, null=True)
    fee =  models.DecimalField(max_digits=15, decimal_places=5, blank=True, null=True)

    def __unicode__(self):
        return self.name

class Administrator(models.Model):
    name = models.CharField(null=True,max_length=50)
    contact_name = models.CharField(null=True,max_length=50)
    contact_number = models.CharField(null=True,max_length=50)
    fee =  models.DecimalField(max_digits=15, decimal_places=5, blank=True, null=True)

    def __unicode__(self):
        return self.name



class Currency(models.Model):
    name = models.CharField(null=True,max_length=50)
    code = models.CharField(null=True,max_length=3)
    def __unicode__(self):
        return self.name

class Country(models.Model):
    name = models.CharField(null=True,max_length=50)
    code = models.CharField(null=True,max_length=3)

    def __unicode__(self):
        return self.name

# deposit, withdrawal, buy sell stocks etc
class TradeType(models.Model):
    pass

class PurchaseSale(models.Model):
    name = models.CharField(null=True,max_length=50)

    def __unicode__(self):
        return self.name

class Alarm(models.Model):
    name = models.CharField(null=True,max_length=50)

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
    name = models.CharField(null=True,max_length=50)


class CounterPartyTrader(models.Model):
    name = models.CharField(null=True,max_length=50)
    counterparty = models.ForeignKey(CounterParty, null=True)

"""
