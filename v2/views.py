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
    # check if this actually works, especially with feb
    #now = datetime.now()
    now = datetime(2013, 12, 5, 6, 22, 45, 517969) # @TODO: remove this later

    months.append(now - timedelta(days=60))
    months.append(now - timedelta(days=30))
    months.append(now)



    MonthlyFormset = formset_factory(FundMonthlyReturnForm, extra=0)
    if request.method == 'POST':
        form = MonthlyFormset(request.POST)

        if form.is_valid():

            for row in form.cleaned_data:

                if row['pk'] == None:
                    continue

                for i in range(2, 4):
                    if row['estimation' + str(i)] == True:
                        try:
                            returns = FundReturnMonthly.objects.get(
                                fund = Fund.objects.get(pk=row['pk']),
                                value_date__year = months[i - 1].year,
                                value_date__month = months[i - 1].month,
                                fund__estimate_required=True,
                            )
                            returns.fund_perf = row['return' + str(i)]
                            returns.save()
                        except:
                            pass

            return HttpResponseRedirect('/admin/fund/returnestimate/')


    # the groups used and their order
    group_qs = AlpheusGroup.objects.all()
    groups = [row.name for row in group_qs]
    
    data = FundReturnMonthly.objects.filter(
        fund__estimate_required=True, value_date__gte=months[0]).\
        order_by('fund__name', 'value_date')

    # set the total nav of all funds
    total = {
        'name': 'Alpheus',
        'nav1': 0,
        'nav2': 0,
        'nav3': 0,
        'weight': 100,
        'return2': 0,
        'return3': 0,
        'ytd': 0,
        'total': True,
    }
    for row in data:
        if row.nav == None:
            continue
        if months[0].month == row.value_date.month:
            total['nav1'] += row.nav
        if months[1].month == row.value_date.month:
            total['nav2'] += row.nav
            if row.fund_perf != None:
                total['return2'] += row.fund_perf
        if months[2].month == row.value_date.month:
            total['nav3'] += row.nav
            total['return3'] += row.fund_perf


    # calculate the values for each fund
    initial = []
    dic = SortedDict()

    for row in data:

        # if a fund doesn't have a group
        if row.fund.group == None:
            continue

        name = row.fund.name
        try:
            dic[name]
        except KeyError:
            dic[name] = {
                'nav1': 0.00,
                'nav2': 0.00,
                'nav3': 0.00,
                'return2': 0,
                'return3': 0,
            }

        for group in groups:

            if group == row.fund.group.name:

                if row.fund_perf == None:
                    fund_perf = 0
                else:
                    fund_perf = row.fund_perf

                dic[name]['pk'] = row.fund.pk
                dic[name]['group'] = group
                dic[name]['total'] = False


                if months[0].month == row.value_date.month:
                    dic[name]['nav1'] = row.nav
                    dic[name]['weight'] = row.nav / total['nav1'] * 100

                if months[1].month == row.value_date.month:
                    try:
                        nav1 = dic[name]['nav1']
                    except:
                        nav1 = 0.00

                    dic[name]['nav2'] = Decimal('%0.2f' % (nav1 + (nav1 * fund_perf)))
                    dic[name]['return2'] = Decimal('%0.2f' % (fund_perf))
                    dic[name]['estimation2'] = row.estimation

                if months[2].month == row.value_date.month:

                    try:
                        nav2 = Decimal(dic[name]['nav2'])
                    except:
                        nav2 = Decimal(0.00)

                    dic[name]['nav3'] = Decimal('%0.2f' % (nav2 + (nav2 * fund_perf)))
                    dic[name]['return3'] = Decimal('%0.2f' % (fund_perf))
                    dic[name]['estimation3'] = row.estimation


                # calculate the ytd data
                ytd_start = date(months[0].year, 1, 1)
                y = months[2].year
                m = months[2].month
                ytd_end = date(y, m, calendar.monthrange(y, m)[1])

                ytd_data = FundReturnMonthly.objects.filter(
                    fund = row.fund, value_date__gte=ytd_start,
                    value_date__lte=ytd_end).\
                    order_by('value_date')
                ytd_lst = []
                for row in ytd_data:
                    if row.fund_perf == None:
                        ytd_lst.append(Decimal(0))
                    else:
                        ytd_lst.append(row.fund_perf)
                
                if ytd_data:        
                    dates = date_range(ytd_lst, ytd_start, 'm')
                    df = to_dataframe(ytd_lst, dates)
                    
                    ytd_val = cum_returns_final_val(df, ytd_lst)
                    ytd_val = ytd_val[0][0]
                else:
                    ytd_val = Decimal(0)
                    
                dic[name]['ytd'] = Decimal('%0.2f' % ytd_val)


    # set the total of each group
    counter = 0
    group_counter = {}
    group_total = {}
    lst_vars = ['nav1', 'nav2', 'nav3', 'weight', 'return2', 'return3']
    for group in groups:
        group_total[group] = {
            'name': '',
            'nav1': 0,
            'nav2': 0,
            'nav3': 0,
            'weight': 0,
            'return2': 0,
            'return3': 0,
            'ytd': 0,
        }
        group_counter[group] = 0
        for row in dic:
            if group == dic[row]['group']:
            
                print group, dic[row]['pk'], row

                # set the location of the first fund in the group
                counter += 1
                if group_counter[group] == 0:
                    group_counter[group] = counter

                for var in lst_vars:
                    try:
                        val = dic[row][var]
                    except:
                        val = 0

                    group_total[group][var] += Decimal(val)

                total['ytd'] += dic[row]['ytd']
                dic[row]['name'] = row

                initial.append(dic[row])

    # modify the list to include the totals of each group
    counter = 1
    for group in groups:
        extra = {
            'name': group,
            'total': True,
            'estimation2': 0,
            'estimation3': 0,
        }
        if group_total[group]['nav1'] != 0 and group_total[group]['nav2'] != 0 \
            and group_total[group]['nav3'] != 0 and group_counter[group] != 0:
            group_total[group].update(extra)
            initial.insert(group_counter[group] - counter, group_total[group])
            print group_counter[group] - counter, group
            counter -= 1

    # insert the total for all groups
    initial.insert(0, total)

    form = MonthlyFormset(initial = initial)

    return render_to_response('admin/fundmonthly.html', {
            'form': form,
            'months': months
        },
        context_instance=RequestContext(request)
    )
