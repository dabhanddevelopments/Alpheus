# myapp/api/resources.py
from django.contrib.auth.models import User
from tastypie.authorization import Authorization
from tastypie import fields
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from api_example.models import Entry
from tastypie.authentication import SessionAuthentication
from tastypie.authorization import DjangoAuthorization
from alpheus.serializers import PrettyJSONSerializer

import random

from tastypie.paginator import Paginator


class MetaPaginator(Paginator):
    def page(self):
        output = super(MetaPaginator, self).page()
        output['meta']['ordering'] = 'username'
        return output
        

      
class UserResource(ModelResource):
    entries = fields.ToManyField('api_example.resources.EntryResource', 'asdf', full=True)
    
    class Meta:
        queryset = User.objects.all().prefetch_related('asdf')
        resource_name = 'user'
        excludes = ['email', 'password', 'is_active', 'is_staff', 'is_superuser']
        filtering = {
            'username': ALL,
        }
        #allowed_methods = ['get', 'post', 'put', 'delete']
        #paginator_class = MetaPaginator
        serializer = PrettyJSONSerializer()
    """    
    def obj_get_list(self, bundle, **kwargs):
        return super(UserResource, self).obj_get_list(bundle, **kwargs).prefetch_related('entry_set')
        
    def alter_list_data_to_serialize2(self, request, data):
        asdf = User.objects.all().prefetch_related('entry_set')
        for test in asdf:
            #print dir(test)
            for whatever in test.entry_set.all():
                print whatever
        print asdf.query
        return data
    """    
    def get_object_list2(self, request):
        return super(UserResource, self).get_object_list(request)[:1]
  


class EntryResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')

    class Meta:
        queryset = Entry.objects.all()
        resource_name = 'entry'
        #authentication = SessionAuthentication()
        authorization = Authorization()
        filtering = {
            'user': ALL_WITH_RELATIONS,
            'pub_date': ['exact', 'lt', 'lte', 'gte', 'gt'],
        }
        allowed_methods = ['get', 'post', 'put', 'delete']

    def obj_create2(self, bundle, request=None, **kwargs):
        return super(EnvironmentResource, self).obj_create(bundle, request, user=request.user)

    def apply_authorization_limits2(self, request, object_list):

        print 'applying auth limits'
        object_list.filter(user=request.user)
        
    def create_random(size=8):
        import string
        import random
        size=8
        
        allowed = string.ascii_letters # add any other allowed characters here 
        randomstring = ''.join([allowed[random.randint(0, len(allowed) - 1)] for x in xrange(size)]) 
        return randomstring      

    def rand_date(self):
        return str(random.randrange(2013, 2014)) + '-' + str(random.randrange(1, 13)) + '-' + str(random.randrange(1, 28))
        
    def alter_list_data_to_serialize(self, request, data):
    
    
        
        from app.models import * 
        
        currency = Currency.objects.all()
        #FxRate.objects.all().delete()
        
        for year in range(2003, 2014):
            for month in range(1, 13):
                for day in range(1,31):
                    for cur in currency:
                    
                        try:
                            fxrate = FxRate(
                                value_date = str(year) + '-' + str(month) + '-1', 
                                currency = cur, 
                                fx_rate = random.randrange(1, 2), 
                            )
                            fxrate.save()
                        except: 
                            pass
                                
        
        benchmark = FundBench.objects.all()
        #FundBenchHist.objects.all().delete()        
        
        for year in range(2003, 2014):
            for month in range(1, 13):
                for bench in range(0, 3):
                    history = FundBenchHist(
                        value_date = str(year) + '-' + str(month) + '-1',    
                        benchmark = benchmark[bench],
                        performance = random.randrange(1, 9),
                        si = random.randrange(1, 9),
                        net_drawdown = random.randrange(-100000,10000000),
                        ann_return1 = random.randrange(0, 5),
                        ann_return3 = random.randrange(0, 5),
                        ann_return5 = random.randrange(0, 5),
                        ann_volatility1 = random.randrange(0, 5),
                        ann_volatility3 = random.randrange(0, 5),
                        ann_volatility5 = random.randrange(0, 5),
                        sharpe_ratio1 = random.randrange(0, 5),
                        sharpe_ratio3 = random.randrange(0, 5),
                        sharpe_ratio5 = random.randrange(0, 5),
                        alpha1 = random.randrange(0, 5),
                        alpha3 = random.randrange(0, 5),
                        alpha5 = random.randrange(0, 5),
                        beta1 = random.randrange(0, 5),
                        beta3 = random.randrange(0, 5),
                        beta5 = random.randrange(0, 5),
                        correlation1 = random.randrange(0, 5),
                        correlation3 = random.randrange(0, 5),
                        correlation5 = random.randrange(0, 5),
                    )
                    history.save()
        #return data
        
        
        
        #return data
        #HoldPerfMonth.objects.all().delete()
        #HoldPerf.objects.all().delete()
        #Alarm.objects.all().delete()
        #CurrencyPositionMonth.objects.all().delete()
        
        #Fund.objects.all().delete()     
        #Holding.objects.all().delete() 
        
        # Holding Peformance
        
        
               
        
        # Fund Peformance
        #FundPerfMonth.objects.all().delete()
        #FundPerf.objects.all().delete()
           
        
        
        holding_categories = HoldingCategory.objects.all()
        
        
        fee = Fee.objects.all()
        
        
        country = Country.objects.all()
        counter_party = CounterParty.objects.all()
        sector = HoldingCategory.objects.filter(holding_group='sec')
        sub_sector = HoldingCategory.objects.filter(holding_group='sub')
        location = HoldingCategory.objects.filter(holding_group='loc')
        asset_class = HoldingCategory.objects.get(id=17) # funds
        holding_names = ['Jupiter Long Short', 'Blackrock Property', \
                'Jupiter Asia Equity',\
                'Jupiter EM Gilts', 'Jupiter EM Equity Long Only'
        ]
        holding_groups = ['sec', 'sub', 'loc', 'ass']
        
        
        # Funds
        
        
        alarm = Alarm(name="alarm1").save()
        
        alarm = Alarm.objects.all()
        fund_type = FundType.objects.all()
        administrator = Administrator.objects.all()
        auditor = Auditor.objects.all()
        classification = Classification.objects.all()
        manager = User.objects.all()
        custodian = Custodian.objects.all()
        
        
        for index in range(0, 1):
            for bench in range(0, 1):
                fund = Fund(
                    name = self.create_random(),
                    counter_party = counter_party[random.randrange(0, 1)],
                    fund_type = fund_type[random.randrange(0, 7)],
                    alarm = alarm[0],
                    benchmark = benchmark[bench],
                    aum = random.randrange(0, 100000),
                    mtd  = random.randrange(0, 5),
                    ytd   = random.randrange(0, 5),
                    #one_day_var  = random.randrange(0, 10),
                    #total_cash = random.randrange(0, 10),
                    #usd_hedge = random.randrange(0, 10),
                    #checks = random.randrange(0, 10),
                    #unsettled = random.randrange(0, 10),
                    custodian = custodian[0],
                    auditor = auditor[0],
                    administrator =  administrator[0],
                    classification = classification[0],
                    manager = manager[0],
                    subscription_frequency = random.randrange(1,5),
                    redemption_frequency = random.randrange(1,5),
                    performance_fee = random.randrange(0, 3), 
                    management_fee =  random.randrange(0, 3),
                    
                    
                )
                fund.save()
        fund = Fund.objects.all()[:1]
             
           
           
           
           

        client_name = [['John', 'Doe'], ['Jane', 'Doe'], ['Juan', 'Nadia'], ['Juanita', 'Ninguna']]
        for name in client_name:
            client = Client(
                first_name = name[0],
                last_name = name[1],
                pending_nav = random.randrange(0,10000000),
                nav = random.randrange(0,10000000),
                no_of_units = random.randrange(0,10000000),
            )
            client.save()
        clients = Client.objects.all() 
        for year in range(2003, 2014):
            for month in range(1, 13):
                for client in range(0, 4):
                    history = ClientPerfMonth(
                        value_date = str(year) + '-' + str(month) + '-1', 
                        fund = fund[0],
                        client = clients[client],
                        performance = random.randrange(1, 5),
                        si = random.randrange(1, 5),
                        ytd = random.randrange(1, 5),
                        net_drawdown = random.randrange(-100000,10000000),
                        ann_return1 = random.randrange(0, 5),
                        ann_return3 = random.randrange(0, 5),
                        ann_return5 = random.randrange(0, 5),
                        ann_volatility1 = random.randrange(0, 5),
                        ann_volatility3 = random.randrange(0, 5),
                        ann_volatility5 = random.randrange(0, 5),
                        sharpe_ratio1 = random.randrange(0, 5),
                        sharpe_ratio3 = random.randrange(0, 5),
                        sharpe_ratio5 = random.randrange(0, 5),
                        alpha1 = random.randrange(0, 5),
                        alpha3 = random.randrange(0, 5),
                        alpha5 = random.randrange(0, 5),
                        beta1 = random.randrange(0, 5),
                        beta3 = random.randrange(0, 5),
                        beta5 = random.randrange(0, 5),
                        correlation1 = random.randrange(0, 5),
                        correlation3 = random.randrange(0, 5),
                        correlation5 = random.randrange(0, 5),
                        previous_nav = random.randrange(0, 1000000),
                        performance_fees_added_back = random.randrange(0, 1000000),
                        subscription_amount = random.randrange(0, 100000),
                        redemption_amount = random.randrange(0, 100000),
                        net_movement = random.randrange(0, 100000),
                        gross_assets_after_subs_red = random.randrange(0, 10000000),
                        pending_nav = random.randrange(0, 1000000),
                        nav = random.randrange(0, 1000000),
                        no_of_units = random.randrange(0, 100000),
                        euro_nav = random.randrange(0, 100000),
       
                    )
                    history.save()           
           
        for year in range(2003, 2014):
            for month in range(1, 13):
                rand = random.randrange(2, 5)
                for index in range(1, rand):
                    sub_red = SubscriptionRedemption(
                        fund = fund[0],
                        client = clients[random.randrange(0, 4)],
                        trade_date = str(year) + '-' + str(month) + '-1', 
                        input_date = str(year) + '-' + str(month) + '-1', 
                        no_of_units = random.randrange(0, 10),
                        sub_red = random.randrange(1, 2),
                        nav = random.randrange(0, 10),
                        percent_released = 1,
                    )
                    sub_red.save()   
          
        # Holdings
        no_holdings = 3
        holding_names = ['Coca Cola', 'Pepsi', 'Pussy']
        for index in range(0, no_holdings):

            name_rand = random.randrange(0, 5)
            
            for holding_name in holding_names:
                
                hold = Holding(
                    name = holding_name,
                    mtd  = random.randrange(0, 5), 
                    fee = fee[random.randrange(0, int(fee.count()))],
                    fund = fund[0],
                    currency = currency[random.randrange(0, int(currency.count()))],
                    country = country[random.randrange(0, int(country.count()))],
                    counter_party = counter_party[random.randrange(0, int(counter_party.count()))],
                    sector = sector[random.randrange(0, int(sector.count()))],
                    sub_sector = sub_sector[random.randrange(0, int(sub_sector.count()))],
                    location = location[random.randrange(0, int(location.count()))],
                    asset_class = asset_class,
                    description = 'n/a',
                    rep_code = 1,
                    isin = 1,
                    valoren = 1,
                    redemption_frequency = random.randrange(1, 4),
                    redemption_notice = 30,
                    max_redemption = random.randrange(10, 50),
                    payment_days = 30,
                    gate = random.randrange(10, 50),
                    soft_lock = random.randrange(1, 2),
                    redemption_fee12 = random.randrange(1, 2),
                    redemption_fee24 = random.randrange(2, 4),
                    redemption_fee36 = random.randrange(3, 5),
                    
                    # historical
                    nav = random.randrange(100000,10000000),
                    value_date = self.rand_date(),
                    dealing_date = self.rand_date(),
                    redemption_date = self.rand_date(),
                    interest_rate = 1,
                    weight = float ('0.' + str(random.randrange(0,99999))),
                    current_price = random.randrange(50,200),
                    no_of_units = random.randrange(1,10000),
                    price_of_unit = random.randrange(1,50),
                    cumulative_nav = random.randrange(1,10000),
                    cumulative_weight = random.randrange(1,100), 
                )
                hold.save()

        trade_types = TradeType.objects.all()
        purchase_sales = PurchaseSale.objects.all()
        holding = Holding.objects.all()
        holding_categories = HoldingCategory.objects.all()

        for index in range(1, 100):
            trade = Trade(
                holding = holding[random.randrange(0, 2)],
                identifier = 1,
                trade_type = trade_types[random.randrange(0, 1)],
                trade_date = self.rand_date(),
                settlement_date = self.rand_date(),
                purchase_sale = purchase_sales[random.randrange(0, 1)], #to be deleted same as buy sell
                buy_sell = random.randrange(1,2),
                no_of_units = random.randrange(50,200),
                purchase_price =random.randrange(50,125),
                purchase_price_base = random.randrange(50,125),
                nav_purchase = random.randrange(50,125),
                currency = currency[random.randrange(0,1)],
                fx_euro = random.randrange(50,100),
                dealing_date = self.rand_date(),
            )
            trade.save()

        for fun in fund:
        
            for year in range(2003, 2014):  
            
                yearly = FundPerfYear(
                    fund = fun, 
                    ytd = random.randrange(1, 9),
                    si = random.randrange(1, 9),
                    value_date = str(year) + '-1-1',
                )
                yearly.save()    
                
                
                for month in range(1, 13):
                
                    print 'start monthly'
                    monthly = FundPerfMonth(
                        fund = fun,
                        year = yearly,
                        ytd = random.randrange(1, 5),
                        si = random.randrange(1, 5),
                        performance = random.randrange(1, 5),
                        net_drawdown = random.randrange(-100000,1000000),
                        ann_return1 = random.randrange(0, 5),
                        ann_return3 = random.randrange(0, 5),
                        ann_return5 = random.randrange(0, 5),
                        ann_volatility1 = random.randrange(0, 5),
                        ann_volatility3 = random.randrange(0, 5),
                        ann_volatility5 = random.randrange(0, 5),
                        sharpe_ratio1 = random.randrange(0, 5),
                        sharpe_ratio3 = random.randrange(0, 5),
                        sharpe_ratio5 = random.randrange(0, 5),
                        alpha1 = random.randrange(0, 5),
                        alpha3 = random.randrange(0, 5),
                        alpha5 = random.randrange(0, 5),
                        beta1 = random.randrange(0, 5),
                        beta3 = random.randrange(0, 5),
                        beta5 = random.randrange(0, 5),
                        correlation1 = random.randrange(0, 5),
                        correlation3 = random.randrange(0, 5),
                        correlation5 = random.randrange(0, 5),
                        euro_nav = random.randrange(0, 10000000),
                        value_date = str(year) + '-' + str(month) + '-1',
                        previous_nav = random.randrange(0, 1000000),
                        performance_fees_added_back = random.randrange(0, 1000),
                        subscription_amount = random.randrange(0, 100000),
                        redemption_amount = random.randrange(0, 10000),
                        net_movement = random.randrange(0, 100000),
                        gross_assets_after_subs_red = random.randrange(0, 1000000),
                        
                        nav_securities = random.randrange(0, 1000000),
                        nav_cash = random.randrange(0, 1000000),
                        nav_other_assets = random.randrange(0, 1000000),
                        
                        administration_fees = random.randrange(0, 10000),
                        audit_fees = random.randrange(0, 10000),
                        capital_payable = random.randrange(0, 10000),
                        corporate_secretarial_fees = random.randrange(0, 1000),
                        custodian_fees = random.randrange(0, 10000),
                        financial_statement_prep_fees = random.randrange(0, 1000),
                        sub_advisory_fees = random.randrange(0, 10000),
                        management_fees = random.randrange(0, 10000),
                        performance_fees = random.randrange(0, 10000),
                        other_liabilities = random.randrange(0, 10000),
                        total_liabilities = random.randrange(0, 100000),
                        
                        no_of_units = random.randrange(1,10000),
                        no_of_units_fund = random.randrange(1,10000),
                        euro_nav_fund = random.randrange(1,10000),
                        nav_securities_total = random.randrange(1,10000),

                        
                    )
                    monthly.save() 
                    
                    
                    for day in range(1, 32):
                    
                        print 'fund', fun, year, month, day
                    
                        daily = FundPerf(
                            fund = fun,
                            month = monthly,
                            performance = random.randrange(1, 9),
                            value_date = str(year) + '-' + str(month) + '-' + str(day)
                        )
                        try:
                            daily.save()
                        except:
                            #raise
                            pass # month with less than 31 days                
     
                            
            #return data                      
            
         
        
        
           

        

        

        for fun in fund:
        
            cur_pos = CurrencyPositionMonth(
                currency = currency[random.randrange(0,1)],
                fund = fun,
                nav = random.randrange(1000,100000),
                value_date = self.rand_date(),
            )
            cur_pos.save()
            
            for year in range(2003, 2014):
            
                for month in range(1, 13):
                
                    for hold in holding:
                    
                        monthly = HoldPerfMonth(
                            fund = fun,
                            holding = hold,
                            performance = random.randrange(1, 9),
                            ytd = random.randrange(1, 9),
                            si = random.randrange(1, 9),
                            value_date = str(year) + '-' + str(month) + '-1', 
                            nav = random.randrange(100000,1000000),
                            weight = float ('0.' + str(random.randrange(0,99999))),
                            #ann_return = random.randrange(0, 10),
                            #ann_volatility = random.randrange(0, 10),
                            #sharpe_ratio = random.randrange(0, 9),
                        )
                        monthly.save() 
     
                    for cat in holding_categories:
                    
                        monthly = HoldPerfMonth(
                            fund = fun,
                            holding = holding[0],
                            holding_category = cat,
                            performance = random.randrange(1, 9),
                            ytd = random.randrange(1, 9),
                            si = random.randrange(1, 9),
                            value_date = str(year) + '-' + str(month) + '-1', 
                            nav = random.randrange(100000,10000000),
                            weight = float ('0.' + str(random.randrange(0,99999))),
                            #ann_return = random.randrange(0, 10),
                            #ann_volatility = random.randrange(0, 10),
                            #sharpe_ratio = random.randrange(0, 9),
                        )
                        monthly.save()          

                        
                        
        for hold in holding:
         
            for year in range(2003, 2014):
            
                for month in range(1, 13):
                    
                    for day in range(1, 32):
                    
                        print hold.id, cat.id, year, month, day
                    
                        daily = HoldPerf(
                            holding = hold,
                            holding_category = cat,
                            month = monthly,
                            #performance = random.randrange(1, 9),
                            nav = random.randrange(100000,10000000),
                            value_date = str(year) + '-' + str(month) + '-' + str(day),
                            interest_rate = 1,
                            weight = float ('0.' + str(random.randrange(0,99999))),
                            current_price = random.randrange(50,120),
                            no_of_units = random.randrange(1,10000),
                            performance = random.randrange(1,5),
                        )
                        try:
                            daily.save()
                        except:
                            pass
            
        return data 
        
        
