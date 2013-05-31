from django.shortcuts import render, render_to_response
from app.models import Menu, Holding, Trade
from django.template import RequestContext
#from django.core.context_processors import csrf
#from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
import calendar
import datetime 
from time import mktime
from alpheus.utils import JsonResponse

from django import template
register = template.Library()
@register.filter()
def last_comma(value, arg):
    return value.replace(arg, ']')

#@method_decorator(ensure_csrf_cookie)
def index(request):
    return render(request, 'index.html')


def check_nodes(request):
    return render(request, 'check-nodes.json', content_type="application/json")

def mainmenu(request):
    return render_to_response("menu.json",
                            {'nodes':Menu.objects.all()},
                            context_instance=RequestContext(request))
                            
def set_columns(column_names, width=False):

    # first column is 0, the rest are 1
    if not width:
        width = {}
        width[0] = 50
        width[1] = 50

    columns = []
    for key, column in enumerate(column_names):
        try: 
            dic = {
                'text': column.title().replace('_', ' '),
                'dataIndex': column,
            }
        except:
            try:
                dic = {
                    'dataIndex': column[0],
                    'text': column[1].title().replace('_', ' '),
                }
            except:
                raise 
        if key == 0:
            dic['width'] = width[0]
        else:
            dic['width'] = width[1]
        columns.append(dic)

    return columns

        



# W1 Data Table
# http://localhost:8000/api/widget/fundperfdatatable/?format=json&fund=2
def fund_perf_data_table(request):

    from models import FundPerfMonth, FundBench
    FundBench.objects.all()
    FundPerfMonth.objects.select_related('fund') 

    fund = request.GET.get('fund', 0)
    
    from models import FundPerfYear
    
    # getting the months using reverse relationship
    years = FundPerfYear.objects.filter(fund=fund).prefetch_related('month')
    
    lis = []
    for year in years:
        dic = {
            'year': year.value_date.year,
            'ytd': year.ytd,
        }
        months = year.month.all()
        for month in months:
            num = month.value_date.month
            
            name = calendar.month_abbr[num]
            dic[name.lower()] = month.performance
        lis.append(dic)

    # create columns
    columns = ['year']
    for month in range(1, 13):
        abbr = calendar.month_abbr[month]
        columns.append(abbr.lower())
    columns.append('ytd') 
    columns = set_columns(columns, [50, 50])

    dic = {
        'sorting': 'year',
        'columns': columns,
        'rows': lis,
    }
    
    return JsonResponse(dic)
    
    

# W6 Fund Historical NAV
# http://localhost:8000/api/widget/fundallochistnav/?format=json&fund=2
def fund_alloc_hist_nav(request):

    fund = request.GET.get('fund', 0)
    
    from models import FundPerfYear
    
    # getting the months using reverse relationship
    years = FundPerfYear.objects.filter(fund=fund).prefetch_related('month')
    
    lis = []
    for year in years:
        dic = {
            'year': year.value_date.year,
            'ytd': year.ytd,
        }
        months = year.month.all()
        for month in months:
            num = month.value_date.month
            
            name = calendar.month_abbr[num]
            dic[name.lower()] = month.euro_nav
        lis.append(dic)

    # create columns
    columns = ['year']
    for month in range(1, 13):
        abbr = calendar.month_abbr[month]
        columns.append(abbr.lower())
    columns.append('ytd') 
    columns = set_columns(columns, [50, 80])

    dic = {
        'sorting': 'year',
        'columns': columns,
        'rows': lis,
    }
    
    return JsonResponse(dic)
    
    
# W16 - Data Table
def fundperfbenchcomptable(request):    

    from models import FundBench, FundPerfMonth, FundBenchHist
                    
    fund = request.GET.get('funds', 0)
    benchmarks = FundBench.objects.filter(funds=fund)
    funds = FundPerfMonth.objects.select_related('fund') \
                        .filter(year__fund=fund).latest('value_date')
 
    # rows
    rows = ['ann_return', 'ann_volatility', 'sharpe_ratio']
    data = []
    for index, row in enumerate(rows):
        dic = {}
        dic['type'] = row.title().replace('_', ' ')
        dic['fund_name'] = getattr(funds, row)
        for index, bench in enumerate(benchmarks):
            history = FundBenchHist.objects \
                                    .filter(benchmark=bench.id) \
                                    .latest('value_date') 
                                                    
            dic['benchmark_' + str(index + 1)] = getattr(history, row)
        data.append(dic)
        
    # get latest SI 
    funds = FundPerfMonth.objects.filter(fund=fund).latest('value_date')
    data.append({'type': 'Since Inception', 'fund_name': funds.si}) 
                
    # columns
    fields = ['type', ['fund_name', funds.fund.name]]
    for index, field in enumerate(benchmarks):
        fields.append('benchmark_' + str(index + 1))  
    columns = set_columns(fields, [100, 100])

    dic = {
        'metaData': {'sorting': 'name'},
        'columns': columns,
        'rows': data,
    }
    return JsonResponse(dic)   
    
    
# W16 - Line Graph & Bar Chart
def fundperfbenchcompline(request):

    from app.models import FundBenchHist, FundPerfMonth

    fund = request.GET.get('fund', 0)
    fields = request.GET.get("fields", 0)

    objects = FundBenchHist.objects.select_related('benchmark').filter(benchmark__fund=fund)

    # benchmarks
    # TODO: redo this
    dic = {}
    for row in objects:        
        date = int(mktime(row.value_date.timetuple())) * 1000
        output = [int(str(date)), row.performance]
        bench_id = int(row.benchmark.id)
        
        try:
            dic[bench_id]['name'] = row.benchmark.name
        except:
            dic[bench_id] = {}
            dic[bench_id]['name'] = row.benchmark.name
        try:
            dic[bench_id]['data'].append(output)
        except:
            dic[bench_id]['data'] = []
            dic[bench_id]['data'].append(output)
            
    response_list = []
    for key, val in dic.iteritems():
        response_list.append(val)
    
    # funds
    funds = FundPerfMonth.objects.select_related('fund') \
                                            .filter(fund=fund)
                
    dic = {}
    for row in funds:        
        date = int(mktime(row.value_date.timetuple())) * 1000
        output = [int(date), row.value] #getattr(row, fields)]
        fund_id = int(row.fund.id)
        
        try:
            dic[fund_id]['name'] = row.fund.name
        except:
            dic[fund_id] = {}
            dic[fund_id]['name'] = row.fund.name
        try:
            dic[fund_id]['data'].append(output)
        except:
            dic[fund_id]['data'] = []
            dic[fund_id]['data'].append(output)
            
    for key, val in dic.iteritems():
        response_list.append(val)
    
    return JsonResponse(response_list)   

