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
    entries = fields.ToManyField('api_example.resources.EntryResource', 'entry_set', related_name='user', full=True)
    
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        excludes = ['email', 'password', 'is_active', 'is_staff', 'is_superuser']
        filtering = {
            'username': ALL,
        }
        allowed_methods = ['get', 'post', 'put', 'delete']
        #paginator_class = MetaPaginator
        serializer = PrettyJSONSerializer()
    



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

    def obj_create(self, bundle, request=None, **kwargs):
        return super(EnvironmentResource, self).obj_create(bundle, request, user=request.user)

    def apply_authorization_limits(self, request, object_list):

        print 'applying auth limits'
        object_list.filter(user=request.user)
        
        
        
  

    def alter_list_data_to_serialize(self, request, data):
    
        import random
        from app.models import * 
        
        
        benchmark = FundBench.objects.all()
        FundBenchHist.objects.all().delete()
         
        for year in range(2002, 2014):
            for month in range(1, 13):
                history = FundBenchHist(
                    value_date = str(year) + '-' + str(month) + '-1',    
                    value = random.randrange(0, 11),
                    benchmark = benchmark[random.randrange(0, 3)],
                    ann_return = random.randrange(0, 10),
                    ann_volatility = random.randrange(0, 10),
                    sharpe_ratio = random.randrange(0, 9),
                )
                history.save()
        #return data
        
        
        
        
        
        
        
        
        
        
        
        
        
        holding = Holding.objects.all().delete()
        holding_categories = HoldingCategory.objects.all()
        fund = Fund.objects.get(id=2)
        
        fee = Fee.objects.all()
        fund = Fund.objects.all()
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
        holding_ids = [1,2,4,5,6]
        holding_groups = ['sec', 'sub', 'loc', 'ass']
               
        
        for year in range(2002, 2014):
            for month in range(1, 13):
                for day in range(1, 32):
                    try: 
                        name_rand = random.randrange(0, 5)
                        holding = Holding(
                            name = holding_names[name_rand],
                            identifier = holding_ids[name_rand],
                            fee = fee[random.randrange(0, int(fee.count()))],
                            fund = fund[random.randrange(0, int(fund.count()))],
                            currency = currency[random.randrange(0, int(currency.count()))],
                            country = country[random.randrange(0, int(country.count()))],
                            counter_party = counter_party[random.randrange(0, int(counter_party.count()))],
                            sector = sector[random.randrange(0, int(sector.count()))],
                            sub_sector = sub_sector[random.randrange(0, int(sub_sector.count()))],
                            location = location[random.randrange(0, int(location.count()))],
                            asset_class = asset_class[random.randrange(0, int(asset_class.count()))],
                            nav = random.randrange(100000,10000000),
                            holding_group = holding_groups[random.randrange(0, 4)],
                            description = 'n/a',                        
                            value_date = str(year) + '-' + str(month) + '-' + str(day),
                            rep_code = 1,
                            isin = 1,
                            valoren = 1,
                            interest_rate = 1,
                            weight = float ('0.' + str(random.randrange(0,99999))),
                            current_price = random.randrange(1,10000),
                            no_of_units = random.randrange(1,10000),
                                                        
                        )
                        holding.save()
                    except:
                        pass
        
                            
                
        #return data
        
        
        
        
        
        
        
        
        
        
        FundPerfYearly.objects.all().delete()
        FundPerfMonthly.objects.all().delete()
        FundPerfDaily.objects.all().delete()
        
        holding = Holding.objects.all()[:5]
        holding_categories = HoldingCategory.objects.all()
        fund = Fund.objects.get(id=2)
        
        for year in range(2002, 2014):
        
            yearly = FundPerfYearly(
                fund = fund,
                holding_group = "all",
                year = year,
                ytd = random.randrange(1, 9),
                si = random.randrange(1, 9),
            )
            yearly.save()    
            
            for month in range(1, 13):
            
                monthly = FundPerfMonthly(
                    fund = fund,
                    holding_group = "all",
                    value = random.randrange(1, 9),
                    year = year,
                    month = month,
                    ann_return = random.randrange(0, 10),
                    ann_volatility = random.randrange(0, 10),
                    sharpe_ratio = random.randrange(0, 9),
                    value_date = str(year) + '-' + str(month) + '-1',
                )
                monthly.save() 
                
                
                for day in range(1, 32):
                
                    daily = FundPerfDaily(
                        fund = fund,
                        value = random.randrange(1, 9),
                        date = str(year) + '-' + str(month) + '-' + str(day)
                    )
                    try:
                        daily.save()
                    except:
                        pass # month with less than 31 days                
                
                    for hold in holding:
                    
                        print year, month, day, hold.name
                        
                        daily = FundPerfDaily(
                            fund = fund,
                            holding = hold,
                            value = random.randrange(1, 9),
                            date = str(year) + '-' + str(month) + '-' + str(day)
                        )
                        try:
                            daily.save()
                        except:
                            pass # month with less than 31 days
                    
                             
            for cat in holding_categories:
                
                yearly = FundPerfYearly(
                    fund = fund,
                    holding_group = cat.holding_group,
                    holding_category = cat,
                    year = year,
                    ytd = random.randrange(1, 9),
                    si = random.randrange(1, 9),
                )
                yearly.save()     
                
                for month in range(1, 13):
                
                    monthly = FundPerfMonthly(
                        fund = fund,
                        holding_group = cat.holding_group,
                        holding_category = cat,
                        value = random.randrange(1, 9),
                        year = year,
                        month = month,
                        value_date = str(year) + '-' + str(month) + '-1',
                        ann_return = random.randrange(0, 10),
                        ann_volatility = random.randrange(0, 10),
                        sharpe_ratio = random.randrange(0, 9),
                    )
                    monthly.save() 
            

                        
        return data                      
            
        
        
        
        
        
        
        
        
                   
        """
        FundPerformanceDaily.objects.all().delete()
        FundPerformanceMonthly.objects.all().delete()
        FundPerformanceYearly.objects.all().delete()
        fund = Fund.objects.get(id=2)
                      
        for year in range(2010, 2014):
        
            yearly = FundPerformanceYearly(
                fund = fund,
                ytd = random.randrange(1, 99),
                si = random.randrange(1, 99),
                year = year,
            )
            yearly.save()
                 
                
            for month in range(1, 13):
            
                monthly = FundPerformanceMonthly(
                    fund = fund,
                    value = random.randrange(1, 99),
                    year = year,
                    month = month,
                    value_date = str(year) + '-' + str(month) + '-1'
                )
                try:
                    monthly.save()
                except:
                    pass # not sure what happened

                
                for day in range(1, 31):
                
                    #print month, day
                    
                    daily = FundPerformanceDaily(
                        fund = fund,
                        value = random.randrange(1, 99),
                        date = str(year) + '-' + str(month) + '-' + str(day)
                    )
                    try:
                        daily.save()
                    except:
                        pass
                    
                            
                            
                            


        return data
        """

