from django.db import models
from django.contrib.auth.models import User
from app.models import DATE_TYPE, ModelBase, Currency, Alarm, Fee, \
                    CounterParty, Custodian, Auditor, Administrator


YES_NO=(
    (1,'Yes'),
    (2,'No'),
)


FREQUENCY=(
    ('m','M'),
    ('q','Q'),
    ('s','SA'),
    ('a','A'),
)

BUY_SELL=(
    (1,'Buy'),
    (2,'Sell'),
)
PERCENT_RELEASED=(
    (90,'90%'),
    (100,'100%'),
)

DATE_TYPE = (
    ('d', 'Day'),
    ('w', 'Week'),
    ('m', 'Month'),
)


class CurrencyPosition(models.Model):
    fund = models.ForeignKey('Fund')
    currency = models.ForeignKey(Currency, related_name='currency_position')
    nav = models.DecimalField(max_digits=20, decimal_places=5,\
                                             blank=True, null=True, verbose_name="NAV")
    base_nav = models.DecimalField(max_digits=20, decimal_places=5)
    euro_nav = models.DecimalField(max_digits=20, decimal_places=5)
    value_date = models.DateField()


class FxRate(models.Model):
    value_date = models.DateField()
    currency = models.ForeignKey(Currency, related_name='currency_fxrate')
    fx_rate = models.DecimalField(max_digits=15, decimal_places=5, blank=True, null=True)

class Classification(models.Model):
    key = models.CharField(max_length=50)
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name


class FundType(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name

from alpheus import utils

class FundBase(ModelBase):

    class Meta:
        abstract = True

    redemption_frequency = models.CharField(max_length=1, blank=True, null=True, choices=FREQUENCY)
    subscription_frequency = models.CharField(max_length=1, blank=True, null=True, choices=FREQUENCY)
    aum = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    mtd = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    ytd = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    administrator_fee = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    performance_fee = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    management_fee = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
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
    no_of_units = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    no_of_units_client = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    no_of_units_fund = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    euro_nav_fund = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    euro_nav_client = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    previous_nav = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True) #last months nav, is this needed? - to keep the same should be previous_euro_nav
    net_movement = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    subscription_amount = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    redemption_amount = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    performance_fee_added_back = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)# not being imported by alexi? input form?
    gross_assets_after_subs_red = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    nav_securities = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    nav_cash = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    nav_other_assets = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    nav_securities_total = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    administrator_fee_payable = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    administrator_fee = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    auditor_fee_payable = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    auditor_fee = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    capital_fee_payable = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    capital_fee = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    corporate_secretarial_payable = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    custodian_fee_payable = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    custodian_management_fee = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    custodian_performance_fee = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    financial_statement_prep_payable = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    sub_advisory_fee_payable = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    management_fee_payable = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    management_fee = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    performance_fee_payable = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    performance_fee = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    other_liabilities_payable = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    total_liabilities = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    total_liabilities_payable = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    assets_liabilities = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    long_portfolio = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    fet_valuation = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True, verbose_name='F.E.T/Valution')
    accrued_interest = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    interest_receivable_on_banks = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    dividends_receivable = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    recv_for_transactions = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    transaction_fee_payable = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True) #is used?
    serv_act_fee_payable = models.DecimalField(max_digits=20, decimal_places=5, \
                                                blank=True, null=True, verbose_name="Payables for Transactions")
    trustee_fee_payable = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    put_options = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    call_options = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    financial_futures  = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    receivables = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    prepaid_or_recov_amounts = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    transitory_assets = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    other_fee = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    commit = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    drawdown = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    various = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    residual_commit = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    distribution = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    valuation = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    total_value = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    net_proceed = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    delta_flow = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    cash_flow = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    irr = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True, verbose_name='IRR')
    description = models.TextField(blank=True, null=True)
    value_date = models.DateField()


    euro_nav = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    pe_total = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    alpheus_cash = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    alpheus_loans = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)


    class Meta:
        abstract = True

class Fund(FundBase):
    fund_type = models.ForeignKey(FundType, related_name="fund_type")
    classification = models.ForeignKey(Classification)
    #counter_party = models.ForeignKey(CounterParty, related_name='fund_cp')
    counter_party = models.ForeignKey(CounterParty)
    alarm = models.ForeignKey(Alarm, blank=True, null=True, related_name='fund_alarm')
    #benchmark = models.ManyToManyField('Benchmark', blank=True, null=True, related_name='fund_benchmark')
    name = models.CharField(max_length=200, null=True)
    alarm = models.ForeignKey(Alarm, blank=True, null=True)
    custodian = models.ForeignKey(Custodian, blank=True, null=True)
    auditor = models.ForeignKey(Auditor, blank=True, null=True)
    administrator =  models.ForeignKey(Administrator, blank=True, null=True)
    classification = models.ForeignKey(Classification, blank=True, null=True, related_name="fund_class")
    manager = models.ForeignKey(User, blank=True, null=True)

    #one_day_var = models.SmallIntegerField()
    #total_cash = models.SmallIntegerField(blank=True, null=True, verbose_name="Total Cash Held in Fund")
    #usd_hedge = models.SmallIntegerField(blank=True, null=True, verbose_name="USD Positions Current FX Hedge")
    #checks = models.SmallIntegerField()
    #unsettled = models.SmallIntegerField()

    def __unicode__(self):
        return self.name



class FundHistory(FundBase):
    fund = models.ForeignKey(Fund)
    date_type = models.CharField(max_length=1, choices=DATE_TYPE)

    class Meta:
        verbose_name = 'Fund history'
        ordering = ['value_date']

class FxHedge(models.Model):
    fund = models.ForeignKey(Fund)
    trade_date = models.DateField()
    settlement_date = models.DateField()
    buy_sell = models.SmallIntegerField(choices=BUY_SELL)
    currency = models.ForeignKey(Currency, related_name='currency_fxhedge')
    amount = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)


class Deposit(models.Model):
    fund = models.ForeignKey(Fund, blank=True, null=True)
    client = models.ForeignKey('client.Client', blank=True, null=True)
    currency = models.ForeignKey(Currency, related_name='currency_deposit')
    trade_date = models.DateField()
    expiration_date = models.DateField()
    amount_base = models.DecimalField(max_digits=20, decimal_places=5)
    deposit_interest_received_base = models.DecimalField(max_digits=20, decimal_places=5)
    deposit_interest_received_euro = models.DecimalField(max_digits=20, decimal_places=5)


