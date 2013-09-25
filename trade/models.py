from django.db import models
from app.models import (
    ModelBase, DATE_TYPE, FREQUENCY, YES_NO, BUY_SELL,
    SUBSCRIPTION_REDEMPTION, Currency, Country, Fee
)



class Trade(models.Model):

    INSTRUCTION_TYPE = (
        ('new', 'New'),
        ('amend', 'Amend'),
        ('cancel', 'Cancellation'),
    )
    FLOW_TYPE = (
        ('inflow', 'Inflow'),
        ('outflow', 'Outflow'),
        ('various', 'Various'),
        ('expense', 'Expense'),
        ('valuation', 'Valuation'),
    )
    OPEN_CLOSE = (
        ('open', 'To Open'),
        ('close', 'To Close'),
    )
    holding = models.ForeignKey('holding.Holding')
    fund = models.ForeignKey('fund.Fund', blank=True, null=True)
    client = models.ForeignKey('client.Client', blank=True, null=True)
    counter_party = models.ForeignKey('app.CounterParty', related_name="counter_party_trade")
    counter_party_trader = models.ForeignKey('app.CounterPartyTrader')
    authorised_by = models.ForeignKey('auth.User', related_name="authorised_by_user")
    buy_sell =  models.SmallIntegerField(choices=BUY_SELL, null=True)
    trade_no = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    desk = models.CharField(max_length=50, blank=True, null=True)
    book = models.CharField(max_length=50, blank=True, null=True)
    bank_reference = models.CharField(max_length=50, blank=True, null=True)
    memorandum_text = models.CharField(max_length=50, blank=True, null=True)
    trade_price_base = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    sub_red_base_nav = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    percent_to_redeem = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    transaction_fees = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    delivery_fees = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    instruction_type = models.SmallIntegerField(max_length=10, choices=INSTRUCTION_TYPE, blank=True, null=True)
    cash_movement = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    trade_slip_no = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    no_of_units = models.DecimalField(max_digits=20, decimal_places=5,\
                                                blank=True, null=True, verbose_name="No. of Units")
    trade_price_euro = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    base_nav = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    euro_nav = models.DecimalField(max_digits=20, decimal_places=5,verbose_name="Euro NAV")
    drawdown_base = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    various_base = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    distribution_base = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    inflow_euro = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    inflow_dollar = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    outflow_euro = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    outflow_dollar = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    fx_euro = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    print_date = models.DateField(blank=True, null=True)
    trade_date = models.DateField(blank=True, null=True)
    dealing_date = models.DateField(blank=True, null=True)
    proceed_date = models.DateField(blank=True, null=True)
    settlement_date = models.DateField(blank=True, null=True)
    instruction_date = models.DateField(blank=True, null=True)
    to_open_to_close = models.CharField(max_length=10, blank=True, null=True, choices=OPEN_CLOSE)
    inflow_outflow_various_expense_valuation = models.CharField(max_length=10, blank=True, null=True, choices=FLOW_TYPE)


    cumulative_euro_nav = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    cumulative_weight = models.DecimalField(max_digits=20, decimal_places=5, blank=True, null=True)
    weight_trade =  models.DecimalField(max_digits=20, decimal_places=5,verbose_name="Weight of Trade")
    corp_action_yes_no = models.SmallIntegerField(choices=YES_NO, null=True)
    transaction_fees = models.DecimalField(max_digits=20, decimal_places=5)
    valuation_base = models.DecimalField(max_digits=20, decimal_places=5)
    valuation_euro = models.DecimalField(max_digits=20, decimal_places=5)
    various_euro = models.DecimalField(max_digits=20, decimal_places=5)
    distribution_euro = models.DecimalField(max_digits=20, decimal_places=5)
    sub_red_cash_movement = models.SmallIntegerField(choices=SUBSCRIPTION_REDEMPTION, null=True)
    percent_to_redeem = models.DecimalField(max_digits=20, decimal_places=5)
    contract_note_received = models.SmallIntegerField(choices=YES_NO, null=True)
