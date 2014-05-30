from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.template import RequestContext  # For CSRF
from django.forms.formsets import formset_factory, BaseFormSet
from django.http import HttpResponse, HttpResponseRedirect
from django.forms.formsets import formset_factory
from django.shortcuts import render_to_response
from v2.forms import  FundMonthlyReturnForm
from v2.models import Fund, FundReturnMonthly, AlpheusGroup
import datetime
from django.db.models import Q
from django.utils.datastructures import SortedDict
from decimal import Decimal
from alpheus.calcs import *
from datetime import date
import calendar

def fund_return_form(request):

    months = []
    # check if this actually works, especially with feb
    now = datetime.datetime.now()
    now = datetime.datetime(2013, 12, 5, 6, 22, 45, 517969) # @TODO: remove this later

    months.append(now - datetime.timedelta(days=60))
    months.append(now - datetime.timedelta(days=30))
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

    for asdf in data:
        print asdf.fund.name
        
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
