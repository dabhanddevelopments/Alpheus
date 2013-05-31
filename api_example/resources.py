# myapp/api/resources.py
from django.contrib.auth.models import User
from tastypie.authorization import Authorization
from tastypie import fields
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from api_example.models import Entry
from tastypie.authentication import SessionAuthentication
from tastypie.authorization import DjangoAuthorization
from alpheus.serializers import PrettyJSONSerializer


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

    def alter_list_data_to_serialize(self, request, data):
    
    
        import random
        from app.models import * 
        
        benchmark = FundBench.objects.all()
        FundBenchHist.objects.all().delete()
         
        for year in range(2006, 2014):
            for month in range(1, 13):
                history = FundBenchHist(
                    value_date = str(year) + '-' + str(month) + '-1',    
                    benchmark = benchmark[random.randrange(0, 3)],
                    performance = random.randrange(1, 9),
                    si = random.randrange(1, 9),
                    ann_return = random.randrange(0, 10),
                    ann_return3 = random.randrange(0, 10),
                    ann_return5 = random.randrange(0, 10),
                    ann_volatility = random.randrange(0, 10),
                    ann_volatility3 = random.randrange(0, 10),
                    ann_volatility5 = random.randrange(0, 10),
                    sharpe_ratio = random.randrange(0, 10),
                    sharpe_ratio3 = random.randrange(0, 10),
                    sharpe_ratio5 = random.randrange(0, 10),
                    alpha = random.randrange(0, 10),
                    alpha3 = random.randrange(0, 10),
                    alpha5 = random.randrange(0, 10),
                    beta = random.randrange(0, 10),
                    beta3 = random.randrange(0, 10),
                    beta5 = random.randrange(0, 10),
                    correlation = random.randrange(0, 10),
                    correlation3 = random.randrange(0, 10),
                    correlation5 = random.randrange(0, 10),
                )
                history.save()
        #return data
        
        
        
        
        
        
        holding = Holding.objects.all().delete()
        holding_categories = HoldingCategory.objects.all()
        
        
        fee = Fee.objects.all()
        
        currency = Currency.objects.all()
        country = Country.objects.all()
        counter_party = CounterParty.objects.all()
        sector = HoldingCategory.objects.filter(holding_group='sec')
        sub_sector = HoldingCategory.objects.filter(holding_group='sub')
        location = HoldingCategory.objects.filter(holding_group='loc')
        asset_class = HoldingCategory.objects.filter(holding_group='ass')
        
        holding_names = ['Jupiter Long Short', 'Blackrock Property', \
                'Jupiter Asia Equity',\
                'Jupiter EM Gilts', 'Jupiter EM Equity Long Only'
        ]
        holding_groups = ['sec', 'sub', 'loc', 'ass']
        
        
        # Funds
        #Fund.objects.all().delete()
        Alarm.objects.all().delete()
        alarm = Alarm(name="alarm1").save()
        
        alarm = Alarm.objects.all()
        fund_type = FundType.objects.all()
        
        for index in range(0, 1):
            fund = Fund(
                name = self.create_random(),
                counter_party = counter_party[random.randrange(0, 1)],
                fund_type = fund_type[random.randrange(0, 7)],
                alarm = alarm[0],
                benchmark = benchmark[random.randrange(0, 3)],
                aum = random.randrange(0, 10),
                mtd  = random.randrange(0, 10),
                ytd   = random.randrange(0, 10),
                one_day_var  = random.randrange(0, 10),
                total_cash = random.randrange(0, 10),
                usd_hedge = random.randrange(0, 10),
                checks = random.randrange(0, 10),
                unsettled = random.randrange(0, 10),
            )
            fund.save()
        fund = Fund.objects.all()[:1]
           
        # Holdings
        for index in range(0, 3):

            name_rand = random.randrange(0, 5)
            holding = Holding(
                name = self.create_random(),
                fee = fee[random.randrange(0, int(fee.count()))],
                fund = fund[random.randrange(0, int(fund.count()))],
                currency = currency[random.randrange(0, int(currency.count()))],
                country = country[random.randrange(0, int(country.count()))],
                counter_party = counter_party[random.randrange(0, int(counter_party.count()))],
                sector = sector[random.randrange(0, int(sector.count()))],
                sub_sector = sub_sector[random.randrange(0, int(sub_sector.count()))],
                location = location[random.randrange(0, int(location.count()))],
                asset_class = asset_class[random.randrange(0, int(asset_class.count()))],
                description = 'n/a',
                rep_code = 1,
                isin = 1,
                valoren = 1,
                
                # historical
                nav = random.randrange(100000,10000000),
                value_date = '2013-01-01',
                interest_rate = 1,
                weight = float ('0.' + str(random.randrange(0,99999))),
                current_price = random.randrange(50,200),
                no_of_units = random.randrange(1,10000),
            )
            holding.save()
        
                            
                
        #return data

        
        
        
        
        
        
        # Fund Peformance
        FundPerfYear.objects.all().delete()
        FundPerfMonth.objects.all().delete()
        FundPerf.objects.all().delete()
        
        for fun in fund:
        
            for year in range(2011, 2014):
            
                yearly = FundPerfYear(
                    fund = fun,
                    value_date = str(year) + str('-01-01'),
                    ytd = random.randrange(1, 9),
                    si = random.randrange(1, 9),
                )
                yearly.save()    
                
                for month in range(1, 13):
                
                    monthly = FundPerfMonth(
                        fund = fun,
                        ytd = random.randrange(1, 9),
                        si = random.randrange(1, 9),
                        performance = random.randrange(1, 9),
                        year = yearly,
                        ann_return = random.randrange(0, 10),
                        ann_return3 = random.randrange(0, 10),
                        ann_return5 = random.randrange(0, 10),
                        ann_volatility = random.randrange(0, 10),
                        ann_volatility3 = random.randrange(0, 10),
                        ann_volatility5 = random.randrange(0, 10),
                        sharpe_ratio = random.randrange(0, 10),
                        sharpe_ratio3 = random.randrange(0, 10),
                        sharpe_ratio5 = random.randrange(0, 10),
                        alpha = random.randrange(0, 10),
                        alpha3 = random.randrange(0, 10),
                        alpha5 = random.randrange(0, 10),
                        beta = random.randrange(0, 10),
                        beta3 = random.randrange(0, 10),
                        beta5 = random.randrange(0, 10),
                        correlation = random.randrange(0, 10),
                        correlation3 = random.randrange(0, 10),
                        correlation5 = random.randrange(0, 10),
                        euro_nav = random.randrange(0, 10),
                        value_date = str(year) + '-' + str(month) + '-1',
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
            
        
        
        
           
        # Holding Peformance
        HoldPerfYear.objects.all().delete()
        HoldPerfMonth.objects.all().delete()
        HoldPerf.objects.all().delete()
        
        holding = Holding.objects.all()
        holding_categories = HoldingCategory.objects.all()
        
        for fun in fund:
            
            for year in range(2011, 2014):
     
                for cat in holding_categories:
                    
                    yearly = HoldPerfYear(
                        fund = fun,
                        holding_category = cat,
                        value_date = str(year) + '-1-1',
                        ytd = random.randrange(1, 9),
                        si = random.randrange(1, 9),
                    )
                    yearly.save()     
                    
                    for month in range(1, 13):
                    
                        monthly = HoldPerfMonth(
                            fund = fun,
                            holding_category = cat,
                            performance = random.randrange(1, 9),
                            year = yearly,
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
         
            for year in range(2011, 2014):
            
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
                            current_price = random.randrange(50,200),
                            no_of_units = random.randrange(1,10000),
                            performance = random.randrange(1,10),
                        )
                        try:
                            daily.save()
                        except:
                            if day < 28:
                                raise
                            else:
                                pass
            
        return data     
                         
