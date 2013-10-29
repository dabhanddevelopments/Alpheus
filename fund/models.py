from django.db import models
from django.contrib.auth.models import User
"""
from app.models import (
    DATE_TYPE, BUY_SELL, ModelBase, Currency, Alarm, Fee,
    Custodian, Auditor, Administrator
)
"""
#from comparative.models import Benchmark, Peer
from alpheus import utils


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

PERCENT_RELEASED=(
    (90,'90%'),
    (100,'100%'),
)


"""
class CurrencyPosition(models.Model):
    fund = models.ForeignKey('Fund', null=True)
    currency = models.ForeignKey(Currency, related_name='currency_position', null=True)
    base_nav = models.DecimalField(null=True,max_digits=20, decimal_places=5)
    euro_nav = models.DecimalField(null=True,max_digits=20, decimal_places=5)
    value_date = models.DateField(null=True)

class FxRate(models.Model):
    value_date = models.DateField(null=True)
    currency = models.ForeignKey(Currency, related_name='currency_fxrate', null=True)
    fx_rate = models.DecimalField(max_digits=15, decimal_places=5, blank=True, null=True)

class Classification(models.Model):
    key = models.CharField(null=True,max_length=50) # not used to be deleted
    name = models.CharField(null=True,max_length=50)
    asset_class = models.ForeignKey('holding.Category', related_name='asset_class_classification', null=True)

    def __unicode__(self):
        return self.name




class FundBase(ModelBase):
    aum = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    mtd = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    ytd = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    si = models.DecimalField(max_digits=20, decimal_places=5, null=True)
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
    no_of_units = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    no_of_units_client = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    no_of_units_fund = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    euro_nav_fund = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    euro_nav_client = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    previous_nav = models.DecimalField(max_digits=20, decimal_places=5, null=True) #last months nav, is this needed? - to keep the same should be previous_euro_nav
    net_movement = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    subscription_amount = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    redemption_amount = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    performance_fee_added_back = models.DecimalField(max_digits=20, decimal_places=5, null=True)# not being imported by alexi? input form?
    gross_assets_after_subs_red = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    nav_securities = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    nav_cash = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    nav_other_assets = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    nav_securities_total = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    administrator_fee_payable = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    auditor_fee_payable = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    auditor_fee = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    capital_fee_payable = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    capital_fee = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    corporate_secretarial_payable = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    custodian_fee_payable = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    custodian_management_fee = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    custodian_performance_fee = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    financial_statement_prep_payable = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    sub_advisory_fee_payable = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    management_fee_payable = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    performance_fee_payable = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    other_liabilities_payable = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    total_liabilities = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    total_liabilities_payable = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    assets_liabilities = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    long_portfolio = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    fet_valuation = models.DecimalField(max_digits=20, decimal_places=5, null=True, verbose_name='F.E.T/Valution')
    accrued_interest = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    interest_receivable_on_banks = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    dividends_receivable = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    recv_for_transactions = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    transaction_fee_payable = models.DecimalField(max_digits=20, decimal_places=5, null=True) #is used?
    serv_act_fee_payable = models.DecimalField(max_digits=20, decimal_places=5, \
                                                null=True, verbose_name="Payables for Transactions")
    trustee_fee_payable = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    put_options = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    call_options = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    financial_futures  = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    receivables = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    prepaid_or_recov_amounts = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    transitory_assets = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    other_fee = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    commit = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    drawdown = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    various = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    residual_commit = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    distribution = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    valuation = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    total_value = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    net_proceed = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    cash_flow_percent_euro_dollar = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    valuation_base = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    irr = models.DecimalField(max_digits=20, decimal_places=5, null=True, verbose_name='IRR')
    value_date = models.DateField(null=True)
    euro_nav = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    pe_total = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    alpheus_cash = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    alpheus_loans = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    custodian_management_fee_payable = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    custodian_performance_fee_payable = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    base_nav = models.DecimalField(null=True,max_digits=20, decimal_places=5,verbose_name="Base NAV")
    weight = models.DecimalField(null=True,max_digits=20, decimal_places=5)
    cash_flow_euro_amount_euro_dollar = models.DecimalField(null=True,max_digits=20, decimal_places=5)
    cash_flow_percent_euro_dollar = models.DecimalField(null=True,max_digits=20, decimal_places=5)

    custodian_management_fee_payable = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    invest_advisors_management = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    invest_advisors_performance = models.DecimalField(max_digits=20, decimal_places=5, null=True)


    class Meta:
        abstract = True

class Fund(FundBase):
    currency = models.ForeignKey(Currency, related_name='currency_fund', null=True)
    alarm = models.ForeignKey(Alarm, null=True, related_name='fund_alarm')
    classification = models.ForeignKey(Classification, null=True, related_name="fund_class")
    administrator =  models.ForeignKey(Administrator, null=True)
    custodian = models.ForeignKey(Custodian, null=True)
    auditor = models.ForeignKey(Auditor, null=True)
    user = models.ForeignKey(User, null=True)
    name = models.CharField(max_length=200, null=True)
    description = models.TextField(null=True)

    code = models.CharField(null=True, max_length=50)
    administrator_fee = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    performance_fee = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    management_fee = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    redemption_frequency = models.CharField(max_length=1, null=True, choices=FREQUENCY)
    subscription_frequency = models.CharField(max_length=1, null=True, choices=FREQUENCY)

    #counter_party = models.ForeignKey(CounterParty, related_name='fund_cp', null=True)
    benchmark = models.ManyToManyField('comparative.Benchmark', null=True)#, related_name='fund_benchmark')
    #one_day_var = models.SmallIntegerField(null=True)
    #total_cash = models.SmallIntegerField(null=True, verbose_name="Total Cash Held in Fund")
    #usd_hedge = models.SmallIntegerField(null=True, verbose_name="USD Positions Current FX Hedge")
    #checks = models.SmallIntegerField(null=True)
    #unsettled = models.SmallIntegerField(null=True)


    def __unicode__(self):
        return self.name



class FundHistory(FundBase):
    fund = models.ForeignKey(Fund)
    date_type = models.CharField(null=True,max_length=1, choices=DATE_TYPE)

    class Meta:
        verbose_name = 'Fund history'
        ordering = ['value_date']

class FxHedge(models.Model):
    fund = models.ForeignKey(Fund, null=True)
    client = models.ForeignKey('client.Client', null=True)
    trade_date = models.DateField(null=True)
    settlement_date = models.DateField(null=True)
    buy_sell = models.SmallIntegerField(null=True,choices=BUY_SELL)
    currency = models.ForeignKey(Currency, related_name='currency_fxhedge', null=True)
    amount_base = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    amount_euro = models.DecimalField(null=True,max_digits=20, decimal_places=5)
    fx_fees = models.DecimalField(max_digits=20, decimal_places=5)
    forward_fx_fees = models.DecimalField(null=True,max_digits=20, decimal_places=5)
    fx_fees_payable = models.DecimalField(max_digits=20, decimal_places=5)
    forward_fx_fees_payable = models.DecimalField(null=True, max_digits=20, decimal_places=5)


class Deposit(models.Model):
    fund = models.ForeignKey(Fund, blank=True, null=True)
    client = models.ForeignKey('client.Client', blank=True, null=True)
    currency = models.ForeignKey(Currency, related_name='currency_deposit', null=True)
    trade_date = models.DateField(null=True)
    expiration_date = models.DateField(null=True)
    amount_base = models.DecimalField(null=True, max_digits=20, decimal_places=5)
    deposit_interest_received_base = models.DecimalField(null=True, max_digits=20, decimal_places=5)
    deposit_interest_received_euro = models.DecimalField(null=True, max_digits=20, decimal_places=5)
    amount_euro = models.DecimalField(null=True, max_digits=20, decimal_places=5)
    deposit_interest_percent = models.DecimalField(null=True, max_digits=20, decimal_places=5)

"""

class Funds(models.Model):
    id = models.AutoField(primary_key=True, db_column='FundID')
    name = models.CharField(max_length=50, db_column='Name', null=True)
    description = models.CharField(max_length=200, db_column='Description', null=True)

    class Meta:
        db_table = 'ALP_Funds'

    def __unicode__(self):
        return self.name



class FundReturnMonthly(models.Model):
    fund = models.ForeignKey(Funds, db_column='FundID', help_text="""The Unique
        ID assigned to the Internal Fund""")
    fund_perf = models.DecimalField(max_digits=18, decimal_places=6,
        db_column='SIFundReturn', help_text="""The monthly performance of the
        fund since its first valuation""", null=True)
    bench_perf = models.DecimalField(max_digits=18, decimal_places=6,
        db_column='SIBenchReturn', help_text="""The monthly performance of the
        fund's benchmark since its first valuation""", null=True)
    value_date = models.DateField(db_column='ValueDate', help_text="""The date
        of the monthly valuation""")
    fund_ytd = models.DecimalField(max_digits=18, decimal_places=6, db_column='YTDFundReturn', null=True)

    class Meta:
        db_table = 'ALP_FundsMonthlyVals_TS'


class FundReturnDaily(models.Model):
    fund = models.ForeignKey(Funds, db_column='FundID', help_text="""The Unique
        ID assigned to the Internal Fund""")
    fund_perf = models.DecimalField(max_digits=18, decimal_places=6,
        db_column='SIFundReturn', help_text="""The monthly performance of the
        fund since its first valuation""", null=True)
    bench_perf = models.DecimalField(max_digits=18, decimal_places=6,
        db_column='SIBenchReturn', help_text="""The monthly performance of the
        fund's benchmark since its first valuation""", null=True)
    value_date = models.DateField(db_column='ValueDate', help_text="""The date
        of the monthly valuation""")
    fund_ytd = models.DecimalField(max_digits=18, decimal_places=6, db_column='YTDFundReturn', null=True)

    class Meta:
        db_table = 'ALP_FundsDailyVals_TS'

