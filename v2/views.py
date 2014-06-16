from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.template import RequestContext  # For CSRF
from django.forms.formsets import formset_factory, BaseFormSet
from django.http import HttpResponse, HttpResponseRedirect
from django.forms.formsets import formset_factory
from django.shortcuts import render_to_response
from v2.forms import  FundMonthlyReturnForm
from v2.models import *
import datetime
from django.db.models import Q
from django.utils.datastructures import SortedDict
from decimal import Decimal
from alpheus.calcs import *
import calendar
from datetime import datetime, date, timedelta
from django.db.models import Sum
from alpheus.utils import set_columns
import json
from django.http import HttpResponse
from operator import itemgetter
from django.db.models import Q
import dateutil.relativedelta

def sub_red(request):

    fund = request.GET.get('fund', False) 
    year = int(request.GET.get('year', datetime.today().year))
    month = int(request.GET.get('month', datetime.today().month))
    
    if fund and month and year:
    
        ct = ClientTransaction.objects.filter(fund=fund, \
                    value_date__year=year, value_date__month=month)
                    
                    
        subscription = ct.filter(buy_sell='b').aggregate(Sum('nav'))['nav__sum']
        
        if subscription == None:
            subscription = 0
            
        redemption  = ct.filter(buy_sell='s').aggregate(Sum('nav'))['nav__sum']
        
        if redemption == None:
            redemption = 0
            
        net_movement = ct.aggregate(Sum('nav'))['nav__sum']
        
        if net_movement == None:
            net_movement = 0
        
        cp = ClientPosition.objects.filter(fund=fund, \
                    value_date__year=year, value_date__month=month) \
                    .aggregate(Sum('market_value'))
                    
        gross_asset = cp['market_value__sum']
        
        if gross_asset == None:
            gross_asset = 0
        
        # change the date to the prior month
        if month == 1:
            year -= year
            month = 12
        else:
            month - 1
            
        cp = ClientPosition.objects.filter(fund=fund, \
                    value_date__year=year, value_date__month=month) \
                    .aggregate(Sum('market_value'))
        
        prev_nav = cp['market_value__sum']
                    
        if prev_nav == None:
            prev_nav = 0
                        
        lis = [{
                'summary': 'Previous NAV',
                'euro': prev_nav,
            }, {
                'summary': 'Subscription Amount',
                'euro': subscription,
            }, {
                'summary': 'Redemption Amount',
                'euro': redemption,
            }, {
                'summary': 'Net Movements',
                'euro': net_movement,
            }, {
                'summary': 'Gross Assets After Subs Reds ',
                'euro': gross_asset,
            }

        ]

        columns = ['summary','euro']
        data = {
            'columns': set_columns(request, columns),
            'rows': lis
        }
        return HttpResponse(json.dumps(data), mimetype="application/json")      
  
  
def nav_reconciliation(request):

    fund = request.GET.get('fund', False) 
    
    if fund:
        
        c = ClientPosition.objects.filter(fund=fund) \
                    .aggregate(Sum('market_value'), Sum('size'))   
        f = FundReturnMonthly.objects.filter(fund=fund) \
                    .aggregate(Sum('shares'), Sum('nav')) 
          
        if c['market_value__sum'] is None:
            c['market_value__sum'] = 0
        if c['size__sum'] is None:
            c['size__sum'] = 0
        if f['nav__sum'] is None:
            f['nav__sum'] = 0
        if f['shares__sum'] is None:
            f['shares__sum'] = 0
         
        data = [[
            float("%.2f" % c['market_value__sum']),
            float("%.2f" % c['size__sum']),
            float("%.2f" % f['nav__sum']),
            float("%.2f" % f['shares__sum']),
        ]]      
        return HttpResponse(json.dumps(data), mimetype="application/json") 
 
def currency_position(request):

    #try:
    fund = Fund.objects.get(id=fund).only('daily_data', 'currency')
    
    if fund.daily_data:
        positions = PositionDaily.filter(~Q(id = fund.currency)) \
                    .aggregate(Sum('marketvaluelcl')) 
    else:
        positions = PositionMonthly.filter(fund=fund).only('')
    
    return HttpResponse(json.dumps(data, indent=4), mimetype="application/json") 

   
def performance_by_fund(request):

    year = request.GET.get('year', False)
    date = request.GET.get('date', 'Year')
    print_version = request.GET.get('print', 'false')

    if year:

        
        months = []
        data = []
        alpheus_total = []
        alpheus_total = {}
        
        # list of months: jan, feb, mar...
        for i in range(1,13):
            months.append(calendar.month_abbr[i].lower())
         
         
        # get the months for the alpheus fund 
        alpheus = FundReturnMonthly.objects.filter(fund__id=1, \
            value_date__year=year).only('nav', 'ytd', 
            'fund__benchpeer__name', 'fund__sec_bench__name') \
            .order_by('value_date')
           
        # default values for alpheus 
        for m in months:
        
            alpheus_total[m] = {
                'val': '-%', 
                'col': 'black',
                'b_val': '-%', 
                'b_col': 'black',
                'sb_val': '-%', 
                'sb_col': 'black'
            }   
                
        # loop through them and set the month values,
        # the ytd, names etc are set by the last value
        for a in alpheus:
        
            month = calendar.month_abbr[a.value_date.month].lower()
            
            if month in months:
            
                try:
                    bench_name = a.fund.benchpeer.name
                except AttributeError:
                    bench_name = 'N/A'
                    
                try:
                    sec_bench_name = a.fund.sec_bench.name
                except AttributeError:
                    sec_bench_name = 'N/A'
                    
                if a.fund_perf < 0:
                    fund_color = 'red'
                else:
                    fund_color = 'blue'
                    
                if a.bench_perf < 0:
                    bench_color = 'red'
                else:
                    bench_color = 'blue'
                    
                    
                if a.ytd < 0:
                    ytd_color = 'red'
                else:
                    ytd_color = 'blue'
                    
                if a.bench_ytd < 0:
                    bench_color = 'red'
                else:
                    bench_color = 'blue'
                    
                if a.sec_bench_ytd < 0:
                    sec_bench_color = 'red'
                else:
                    sec_bench_color = 'blue'

        
                try:
                    fund_perf = str("%.2f" % a.fund_perf) + '%'
                except TypeError:
                    fund_perf = '-%'
                    
                try:
                    bench_perf = str("%.2f" % a.bench_perf) + '%'
                except TypeError:
                    bench_perf = '-%'
                    
                try:
                    sec_bench_perf = str("%.2f" % a.sec_bench) + '%'    
                except TypeError:
                    sec_bench_perf = '-%'
           
        
                alpheus_total[month] = {
                    'val': fund_perf, 
                    'col': fund_color,
                    'b_val': bench_perf, 
                    'b_col': bench_color,
                    'sb_val': sec_bench_perf, 
                    'sb_col': sec_bench_color
                }
        
                ytd = a.ytd
                bench_ytd = a.bench_ytd
                sec_bench_ytd = a.sec_bench_ytd
                weight = '100%'
        
        if len(alpheus) == 0:
            weight = 'N/A'
            ytd = 0
            bench_ytd = 0
            sec_bench_ytd = 0
            ytd_color = 'black'
            bench_color = 'black'
            sec_bench_color = 'black'
            bench_name = 'N/A'
            sec_bench_name = 'N/A'
            
        #alpheus_total.append(alpheus_months)        
        #alpheus_total.append({
        try:
            alpheus_total['ytd'] = {'val': str("%.2f" % ytd) + '%', 'col': ytd_color}
        except TypeError:
            alpheus_total['ytd'] = {'val': str("%.2f" % 0) + '%', 'col': 'black'}
            
        alpheus_total['weight'] = {'val': weight, 'col': 'blue'}
        
        try:
            alpheus_total['bench_name'] = bench_name
        except TypeError:
            alpheus_total['bench_name'] = 'N/A' 
            
        try:
            alpheus_total['sec_bench_name'] = sec_bench_name
        except TypeError:
            alpheus_total['sec_bench_name'] = 'N/A'
            
        try:
            alpheus_total['bench_ytd'] = {
                'val': str("%.2f" % bench_ytd) + '%', 
                'col': bench_color
            }
        except TypeError:
            alpheus_total['bench_ytd'] = {
                'val': str("%.2f" % 0) + '%', 
                'col': 'black'
            }
            
        try:
            alpheus_total['sec_bench_ytd'] = {
                'val': str("%.2f" % sec_bench_ytd) + '%', 
                'col': sec_bench_color
            }
        except TypeError:
            alpheus_total['sec_bench_ytd'] = {
                'val': str("%.2f" % 0) + '%', 
                'col': 'black'
            }
        
    
        # get the groups and their order
        groups = AlpheusGroup.objects.all().order_by('pk')
                    
        # the rest of the groups
        for group in groups:
        
            group_data = []
            
            try:
            
                # get the latest value of the year
                latest = FundReturnMonthly.objects.filter(fund__group=group, \
                             fund__estimate_required=True, value_date__year=year) \
                             .order_by('-value_date').only('value_date')[0]
                
                # get the values for the latest month
                returns = FundReturnMonthly.objects.filter(fund__group=group, \
                   fund__estimate_required=True, value_date=latest.value_date) \
                   .only('fund__id', 'fund__name', 'nav', 'ytd',
                            'bench_ytd', 'fund__benchpeer__name')
                   
            except IndexError:
                continue
                
            try:             
                # get the NAV for the alpheus fund's latest month
                alpheus = FundReturnMonthly.objects.filter(fund__id=1, \
                                value_date=latest.value_date).only('nav')[0]
                alpheus_nav = alpheus.nav
            except IndexError:
                alpheus_nav = 0
               

                            
            fund_order = []
            
            for r in returns:
                
                # calculate the weight from the two NAV values
                try:
                    weight = ((r.nav / alpheus_nav) * 100),
                    weight = str("%.2f" % weight) + '%'
                except:
                    weight = 'N/A'
                  
                # some funds don't have a benchmark
                try:
                    bench_name = r.fund.benchpeer.name
                except AttributeError:
                    bench_name = 'N/A'
                    
                if r.ytd < 0:
                    ytd_color = 'red'
                else:
                    ytd_color = 'blue'
                    
                if r.bench_ytd < 0:
                    bench_color = 'red'
                else:
                    bench_color = 'blue'
                    
                if weight < 0:
                    weight_color = 'red'
                else:
                    weight_color = 'blue'
                    
                try:
                    fund_order.append({
                        'fund_id': r.fund.id,
                        'fund_name': r.fund.name,
                        'ytd': {'val': str("%.2f" % r.ytd) + '%', 'col': ytd_color},
                        'weight': {'val': weight, 'col': weight_color},
                        'bench_name': bench_name,
                        'bench_ytd': {'val': str("%.2f" % r.bench_ytd) + '%', 'col': bench_color},
                    })
                except TypeError:
                    pass
            
            bench = {}
            
            # sort the fund ids by weight
            sorted_funds = sorted(fund_order, key=itemgetter('weight'), reverse=True) 
            
            for sort in sorted_funds:
            
                # get the fund performance for the whole year
                returns = FundReturnMonthly.objects.filter(fund__id=sort['fund_id'], \
                      value_date__year=year) \
                      .only('fund_perf', 'estimation', 'bench_perf')
                      
                # fill dict with default values that we later over write
                for m in months:
                
                    sort[m] = {
                        'val': '-%', 
                        'col': 'black',
                        'b_val': '-%', 
                        'b_col': 'black'
                    }              
                
                # appending the fund performance for each month of this year
                for r in returns:
                
                    month = calendar.month_abbr[r.value_date.month].lower()
                    
                    if month in months:
                    
                        if r.fund_perf < 0:
                            fund_color = 'red'
                        else:
                            fund_color = 'blue'
                            
                        if r.bench_perf < 0:
                            bench_color = 'red'
                        else:
                            bench_color = 'blue'
                            
                        fund_perf = str("%.2f" % r.fund_perf) + '%'
                        bench_perf = str("%.2f" % r.bench_perf) + '%'
                        
                        if r.estimation == 1:
                            fund_perf += ' e'   
                        
                    #group_data.append({month: perf})
                    sort[month] = {
                        'val': fund_perf, 
                        'col': fund_color,
                        'b_val': bench_perf, 
                        'b_col': bench_color
                    }
                    
                group_data.append(sort)
            
            data.append({
                'group': group.name,
                'data': group_data,
            })
        #return HttpResponse(json.dumps(data, indent=4), mimetype="application/json") 
        #assert False
        
        return render_to_response('admin/performance_by_fund.html', {
                'data': data,
                'date': date,
                'print': print_version,
                'a': alpheus_total,
            },
            context_instance=RequestContext(request)
        )
    else:
    
        return HttpResponse('No year paramater passed')
        
def fund_return_form(request):

    months = []
    prior_months = []
    # check if this actually works, especially with feb
    #now = datetime.now()
    now = datetime(2011, 12, 5, 6, 22, 45, 517969) # @TODO: remove this later

    # make the 'now' date the last day of the month
    now = datetime(now.year, now.month, calendar.monthrange(now.year, now.month)[1])
    
    months.append(now - dateutil.relativedelta.relativedelta(months=1))
    months.append(now)
    prior_months.append(now - dateutil.relativedelta.relativedelta(months=2))
    prior_months.append(now - dateutil.relativedelta.relativedelta(months=1))


    MonthlyFormset = formset_factory(FundMonthlyReturnForm, extra=0)
    if request.method == 'POST':
        form = MonthlyFormset(request.POST)

        if form.is_valid():

            for row in form.cleaned_data:
            
                for i in range(1, 3):
                
                    pk = row['pk' + str(i)]
                    fund = row['fund']
                    estimation = row['return' + str(i)]
                    
                    if estimation != None:
                            
                        returns = FundReturnMonthly(pk=pk)
                        
                        try:
                            prior_returns = FundReturnMonthly.objects.get(
                                fund__id = row['fund'],
                                value_date__year = prior_months[i - 1].year,
                                value_date__month = prior_months[i - 1].month,
                                fund__estimate_required=True,
                            ).only('nav')
                            prior_nav = prior_returns.nav
                        except:
                            prior_nav = 0
                            
                        returns.nav = prior_nav + \
                            (prior_nav * estimation / 100) 
                        returns.fund = Fund.objects.get(pk=fund)
                        returns.value_date = months[i - 1]
                        returns.fund_perf = estimation
                        returns.estimation = True
                        returns.save()

            return HttpResponseRedirect('/admin/fund/returnestimate/')


    # the groups used and their order
    group_data = AlpheusGroup.objects.all()
    
    alpheus_qs = FundReturnMonthly.objects.only('fund_perf')

    try:
        month = alpheus_qs.filter(value_date=months[0]) \
            .aggregate(Sum('fund_perf'))['fund_perf__sum']
        prior_month = alpheus_qs.filter(value_date=months[1]) \
            .aggregate(Sum('fund_perf'))['fund_perf__sum']
        return1 = ((month - prior_month) / prior_month) * 100
    except:
        return1 = 0
        
    try:
        month = alpheus_qs.filter(value_date=months[1]) \
            .aggregate(Sum('fund_perf'))['fund_perf__sum']
        prior_month = alpheus_qs.filter(value_date=months[1]) \
            .aggregate(Sum('fund_perf'))['fund_perf__sum']
        return2 = (month - prior_month) / month * 100
    except:
        return2 = 0
        
    data = [{
        'name': 'Alpheus',
        'group': True,
    }]
    data.append({
        'name': 'Alpheus',
        'return1': return1,
        'return2': return2,
    })
    for group in group_data:
    
        funds = Fund.objects.filter(group=group, estimate_required=True) \
                                        .order_by('name').only('id', 'name')
        if funds:    
            data.append({
                'name': group.name,
                'group': True,
            })
            
        for fund in funds:
        
            fund_row = {}
            fund_row['name'] = fund.name
            fund_row['fund'] = fund.id
            
            try:
                returns = FundReturnMonthly.objects.filter(fund=fund,
                    value_date__gte=months[0], value_date__lte=months[1])\
                    .order_by('value_date').only('id', 'fund_perf', 'estimation')
            except:
                pass

            try:
                fund_row['return1'] = returns[0].fund_perf
                fund_row['estimation1'] = returns[0].estimation 
                fund_row['pk1'] = returns[0].id
            except:
                fund_row['input1'] = True
            try:
                fund_row['return2'] = returns[1].fund_perf
                fund_row['estimation2'] = returns[1].estimation
                fund_row['pk2'] = returns[1].id
            except:
                fund_row['input2'] = True

            data.append(fund_row)

    form = MonthlyFormset(initial = data)
    
    return render_to_response('admin/fundmonthly.html', {
            'form': form,
            'month1': months[0],
            'month2': months[1],
        },
        context_instance=RequestContext(request)
    )
