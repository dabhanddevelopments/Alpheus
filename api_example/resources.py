# myapp/api/resources.py
from django.contrib.auth.models import User
from tastypie.authorization import Authorization
from tastypie import fields
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from api_example.models import Entry
from tastypie.authentication import SessionAuthentication
from tastypie.authorization import DjangoAuthorization


from tastypie.paginator import Paginator


class MetaPaginator(Paginator):
    def page(self):
        output = super(MetaPaginator, self).page()
        output['meta']['ordering'] = 'username'
        return output
        


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        excludes = ['email', 'password', 'is_active', 'is_staff', 'is_superuser']
        filtering = {
            'username': ALL,
        }
        allowed_methods = ['get', 'post', 'put', 'delete']
        paginator_class = MetaPaginator


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
        
        FundPerfYearly.objects.all().delete()
        FundPerfMonthly.objects.all().delete()
        FundPerfDaily.objects.all().delete()
        
        holding = Holding.objects.all()
        holding_categories = HoldingCategory.objects.all()
        fund = Fund.objects.get(id=1)
    
        
        for year in range(2010, 2014):
        
            yearly = FundPerfYearly(
                fund = fund,
                holding_group = "all",
                year = year,
                ytd = random.randrange(1, 99),
                si = random.randrange(1, 99),
            )
            yearly.save()    
            
            for month in range(1, 13):
            
                monthly = FundPerfMonthly(
                    fund = fund,
                    holding_group = "all",
                    value = random.randrange(1, 99),
                    year = year,
                    month = month,
                )
                monthly.save() 
                
                
                for day in range(1, 32):
                
                    daily = FundPerfDaily(
                        fund = fund,
                        value = random.randrange(1, 99),
                        date = str(year) + '-' + str(month) + '-' + str(day)
                    )
                    try:
                        daily.save()
                    except:
                        pass # month with less than 31 days                
                
                    for hold in holding:
                    
                        print hold.name, year, month, day
                        
                        daily = FundPerfDaily(
                            fund = fund,
                            holding = hold,
                            value = random.randrange(1, 99),
                            date = str(year) + '-' + str(month) + '-' + str(day)
                        )
                        try:
                            daily.save()
                        except:
                            pass # month with less than 31 days
                    
                             
            for cat in holding_categories:
                
                yearly = FundPerfYearly(
                    fund = fund,
                    holding_group = "sec",
                    holding_category = cat,
                    year = year,
                    ytd = random.randrange(1, 99),
                    si = random.randrange(1, 99),
                )
                yearly.save()     
                
                for month in range(1, 13):
                
                    monthly = FundPerfMonthly(
                        fund = fund,
                        holding_group = "sec",
                        holding_category = cat,
                        value = random.randrange(1, 99),
                        year = year,
                        month = month,
                    )
                    monthly.save() 
            

                        
                            
        return data     
        
        
        
        
        
        
        
        
        
        
                   

        FundPerformanceDaily.objects.all().delete()
        FundPerformanceMonthly.objects.all().delete()
        FundPerformanceYearly.objects.all().delete()
        fund = Fund.objects.get(id=1)
                      
        for year in range(2006, 2014):
        
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


