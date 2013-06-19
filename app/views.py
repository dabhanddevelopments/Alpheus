from django.shortcuts import render, render_to_response
from app.models import Menu, Holding, Trade
from django.template import RequestContext
#from django.core.context_processors import csrf
#from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
import calendar
from datetime import date
from time import mktime
from alpheus.utils import JsonResponse
from operator import itemgetter

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

def get_month_list():
    months = []
    for month in range(1, 13):
        months.append(calendar.month_abbr[month].lower())
    return months

def set_columns(request, column_names):

    column_width = request.GET.get('column_width', '50,50').split(',')
    column_border_y = request.GET.get('column_border_y', 'ytd')
    align = request.GET.get('align', 'left')

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
                
        if column == column_border_y:
            dic['tdCls'] = 'horizonal-border-column'
        
        if key == 0:
            dic['width'] = column_width[0]
        else:
            dic['width'] = column_width[1]
            dic['align'] = align
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
    columns = set_columns(request, columns)

    dic = {
        'sorting': 'year',
        'columns': columns,
        'rows': sorted(lis, key=itemgetter('year'), reverse=True),
    }

    return JsonResponse(dic)


# W6 Fund Historical NAV
# http://localhost:8000/api/widget/fundallochistnav/?format=json&fund=2
def fundallochistnav(request):

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
    columns = set_columns(request, columns)

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
    rows = ['ann_return1', 'ann_volatility1', 'sharpe_ratio1']
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
    columns = set_columns(request, fields)

    dic = {
        'metaData': {'sorting': 'name'},
        'columns': columns,
        'rows': data,
    }
    return JsonResponse(dic)


# W16 - Line Graph & Bar Chart
# http://localhost:8010/api/widget/fundperfbenchcompline/?fund=2&fields=performance&format=json
def fundperfbenchcompline(request):

    from app.models import FundBenchHist, FundPerfMonth

    fund = request.GET.get('fund', 0)
    fields = request.GET.get("fields", 0)

    objects = FundBenchHist.objects.select_related('benchmark').filter(benchmark__funds=fund)

    # benchmarks
    # TODO: redo this
    dic = {}
    for row in objects:
        date = int(mktime(row.value_date.timetuple())) * 1000
        output = [int(date), row.performance]
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
        output = [int(date), getattr(row, fields)]
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
        print val
        response_list.append(val)

    return JsonResponse(response_list)

# W19 Fund Return Table
# http://localhost:8010/api/widget/fundreturn/?format=json&fund=2
def fundreturn(request):

    from app.models import FundPerfMonth, FundBenchHist

    fund = request.GET.get('fund', 0)

    # Last month of year is the yearly value
    funds = FundPerfMonth.objects.select_related('fund') \
                            .filter(value_date__month=12, fund=fund)
    benchmarks = FundBenchHist.objects.select_related('benchmark') \
                            .filter(value_date__month=12, benchmark__funds=fund)
    dic = {}

    # funds
    fund_column = ['year']
    for year in range(1970, date.today().year + 1):
        dic[year] = {}
        for row in funds:
            if year == row.value_date.year:
                dic[year][row.fund.name] = row.performance  # change to: ytd
                if row.fund.name not in fund_column:
                    fund_column.append(row.fund.name)
    # benchmarks
    bench_columns = []
    for year in range(1970, date.today().year + 1):
        for row in benchmarks:
            if year == row.value_date.year:
                dic[year][row.benchmark.name] = row.performance # change to: ytd
                if row.benchmark.name not in bench_columns:
                    bench_columns.append(row.benchmark.name)

    # sort the bench columns by name
    columns = fund_column + sorted(bench_columns)

    result = []
    for key, val in dic.iteritems():
        if val:
            val['year'] = key
            result.append(val)

    dic = {
        'metaData': {'sorting': 'year'},
        'columns': set_columns(request, columns),
        'rows': sorted(result, key=itemgetter('year'), reverse=True),
    }
    return JsonResponse(dic)

def fundbestworst(request):

    from app.models import FundPerfMonth, FundBenchHist
    from django.db.models import Max, Min, Avg, Count

    fund = request.GET.get('fund', 0)

    columns = ['best_worst_months']
    positive = {'best_worst_months': 'Positive Months'}
    lis = []

    """ Number of months that are positive """

    # Positive Fund Months
    f = FundPerfMonth.objects.select_related('fund').filter(value_date__month=12, fund=fund)
    p = f.filter(performance__gt=0)
    fund_name = f.values('fund__name')[0]['fund__name']
    positive[fund_name] = p.count() / f.count() * 100
    columns.append(fund_name)

    # Positive Benchmark Months
    b = FundBenchHist.objects.filter(value_date__month=12,
                                     benchmark__funds=fund) \
                                    .values('benchmark__name', 'benchmark__id') \
                                    .annotate(count=Count('value_date')) \
                                    .order_by('benchmark__name')
    b2 = b.filter(performance__gt=0)

    for bench in b:
        pos_count = 0
        for pos in b2:
            if pos['benchmark__id'] == bench['benchmark__id']:
                pos_count = pos['count']

        positive[bench['benchmark__name']] = float(pos_count) / float(bench['count']) * 100
        columns.append(bench['benchmark__name'])
    lis.append(positive)

    # Best, Worst & Draw Down
    best = {'best_worst_months': 'Best Monthly Return'}
    worst = {'best_worst_months': 'Worst Monthly Return'}
    drawdown = {'best_worst_months': 'Worst Drawdown'}
    funds = FundPerfMonth.objects.filter(value_date__month=12, fund=fund) \
                            .values('fund__name') \
                            .annotate(Max('performance'), Min('performance'),
                                Min('net_drawdown')) \
                            .order_by('fund__name')
    for row in funds:
        best[row['fund__name']] = row['performance__max']
        worst[row['fund__name']] = row['performance__min']
        drawdown[row['fund__name']] = row['net_drawdown__min']

    benchmarks = FundBenchHist.objects.filter(
                         value_date__month=12, benchmark__funds=fund) \
                                .values('benchmark__name') \
                                .annotate(Max('performance'), Min('performance'),
                                    Min('net_drawdown')) \
                                .order_by('benchmark__name')
    for bench in benchmarks:
        best[bench['benchmark__name']] = bench['performance__max']
        worst[bench['benchmark__name']] = bench['performance__min']
        drawdown[bench['benchmark__name']] = bench['net_drawdown__min']
    lis.append(best)
    lis.append(worst)
    lis.append(drawdown)

    dic = {
        'metaData': {'sorting': 'year'},
        'columns': set_columns(request, columns),
        'rows': lis,
    }
    return JsonResponse(dic)


def fundreturnhistogram(request):

    from app.models import FundPerfMonth
    from django.db.models import Count

    fund_id = request.GET.get('fund', 0)

    lis = []
    columns = ['+10%', '5 to 10%', '4%', '3%', '2%', '1%', '0%',
                   '-1%', '-2%', '-3%', '-4%', '-5 to 10%', '-10%']

    funds = FundPerfMonth.objects.filter(fund=fund_id)

    # get 10+
    count = funds.filter(performance__gte=10).aggregate(Count('performance'))
    lis.append([columns[0], count['performance__count']])

    # get 5 to 10
    count = funds.filter(performance__gte=5, performance__lt=10) \
                                        .aggregate(Count('performance'))
    lis.append([columns[1], count['performance__count']])

    # get -5 to +5
    # @TODO: On MSSQL SIGNED is called INT
    sql = """
    SELECT id,
        Cast(performance as SIGNED) as performance,
        Count(performance) as count
    FROM app_fundperfmonth
    WHERE fund_id = %s
        AND performance > -5 AND performance < 5
    GROUP BY Cast(performance as SIGNED)
    ORDER BY performance DESC;
    """
    raw = FundPerfMonth.objects.raw(sql, [fund_id])
    dic = {}
    for fund in raw:
        dic[str(fund.performance)] = fund.count
    for index in range(4, -5, -1):
        try:
            count = dic[str(index)]
            print count
        except:
            count = 0
        lis.append([str(index) + '%', count])

    # get -5 to -10
    count = funds.filter(performance__gte=5, performance__lt=10).aggregate(Count('performance'))
    lis.append([columns[11], count['performance__count']])

    # get -10 and Lower
    count = funds.filter(performance__gte=10).aggregate(Count('performance'))
    lis.append([columns[12], count['performance__count']])

    dic = {
        'columns': columns,
        'objects': [{'data': lis}]
    }
    return JsonResponse(dic)


def fundcorrelationmatrix(request):

    from app.models import FundPerfMonth, FundBench

    fund_id = request.GET.get('fund', 0)

    # Get the latest values
    fund = FundPerfMonth.objects.select_related('fund').filter(fund=fund_id) \
                                        .latest('value_date')
    benchmarks = FundBench.objects.filter(funds=fund_id)

    columns = ['Correlation Matrix', fund.fund.name]
    lis = []
    dic = {}

    # fund correlation
    dic['Correlation Matrix'] = fund.fund.name
    dic[fund.fund.name] = fund.performance / fund.performance
    for bench in benchmarks:
        dic[bench.name] = fund.performance / bench.mtd
    lis.append(dic)

    # benchmark correlation
    for col in benchmarks:
        dic = {}
        for row in benchmarks:
            dic[row.name] = row.mtd / col.mtd
        dic['Correlation Matrix'] = col.name
        dic[fund.fund.name] = fund.performance / col.mtd
        lis.append(dic)
        columns.append(col.name)

    dic = {
        'columns': set_columns(request, columns),
        'rows': lis
    }
    return JsonResponse(dic)


def holdcorrelationmatrix(request):

    from app.models import Holding

    fund_id = request.GET.get('fund', 0)

    holdings = Holding.objects.filter(fund=fund_id)

    columns = ['Correlation Matrix']
    lis = []
    for col in holdings:
        dic = {}
        for row in holdings:
            try:
                dic[row.name] = row.mtd / col.mtd
            except:
                dic[row.name] = 0
        dic['Correlation Matrix'] = col.name
        lis.append(dic)
        columns.append(col.name)

    dic = {
        'columns': set_columns(request, columns),
        'rows': lis
    }
    return JsonResponse(dic)

def fundnegativemonths(request):

    from app.models import FundPerfMonth, FundBenchHist
    from django.db.models import Avg

    fund_id = request.GET.get('fund', 0)
    type_id = request.GET.get('fund', 0)

    funds = FundPerfMonth.objects.filter(fund=fund_id) \
                                    .values('fund__name') \
                                    .annotate(Avg('performance')) \
                                    .order_by('fund__name')[0]
    dic = {
        funds['fund__name']: funds['performance__avg'],
    }

    benchmarks = FundBenchHist.objects.filter(benchmark__funds=fund_id,
                                     performance__gt=0) \
                                    .values('benchmark__name') \
                                    .annotate(Avg('performance')) \
                                    .order_by('benchmark__name')
    for bench in benchmarks:
        dic[bench['benchmark__name']] = bench['performance__avg']

    columns = [key for key, val in dic.iteritems()]

    return dic, columns

def fundnegativemonthstable(request):

    dic, columns = fundnegativemonths(request)
    avg_perf = 'Avg Performance in neg months'
    dic[avg_perf] = 'Avg Performance'
    columns = [avg_perf] + columns

    data = {
        'columns': set_columns(request, columns),
        'rows': [dic]
    }
    return JsonResponse(data)

def fundnegativemonthsgraph(request):

    dic, columns = fundnegativemonths(request)
    lis = [[key, val] for key, val in dic.iteritems()]

    data = {
        'columns': columns,
        'objects': [{'data': lis}]
    }
    return JsonResponse(data)

def currencyhedge(request):

    from app.models import CurrencyPositionMonth, FxHedge, FxRate
    from django.db.models import Sum
    fund_id = request.GET.get('fund', 0)

    sql = """
        SELECT id, currency_id, amount, settlement_date
        FROM `app_fxhedge`
        WHERE (`app_fxhedge`.`fund_id` = %s  AND `app_fxhedge`.`settlement_date` > %s )
        GROUP BY `app_fxhedge`.`currency_id`
        ORDER BY `app_fxhedge`.`settlement_date` ASC
    """
    fx = FxHedge.objects.raw(sql, [fund_id, date.today()])
    lis = []
    for row in fx:
       perf = CurrencyPositionMonth.objects.select_related('currency') \
                        .filter(fund=fund_id, currency=row.currency_id) \
                        .latest('value_date')
       fxrate = FxRate.objects.filter(currency=row.currency_id).latest('value_date')

       try:
           euro_eq = (perf.nav - row.amount) / fxrate.fx_rate
       except:
           euro_eq = 0

       dic = {
         'currency': perf.currency.name,
         'total_position': perf.nav,
         'total_hedge': row.amount,
         'hedge_expires': str(row.settlement_date),
         'exposure': perf.nav - row.amount,
         'euro_equivalent': euro_eq,
       }
       lis.append(dic)
    columns = ['currency', 'total_position', 'total_hedge', 'hedge_expires', 'exposure', 'euro_equivalent', ]
    data = {
        'columns': set_columns(request, columns),
        'rows': lis
    }
    return JsonResponse(data)


def subscriptionredemption(request):

    from app.models import SubscriptionRedemption
    fund = request.GET.get('fund', 0)
    client = request.GET.get('client', 0)
    queryset = SubscriptionRedemption.objects.filter(fund=fund, client=client)
    lis = []
    for row in queryset:
        dic = {
            'sub_red': row.get_sub_red_display(),
            'percent_released': row.get_percent_released_display(),
            'trade_date': str(row.trade_date),
            'no_of_units': row.no_of_units,
            'nav': row.nav


        }
        lis.append(dic)

    columns = [['sub_red', 'Sub. or Red.'], 'trade_date',
               ['no_of_units', 'No. of Units'], ['nav', 'NAV of Trance'],
               'percent_released']
    data = {
        'metaData': {'sorting': 'name'},
        'columns': set_columns(request, columns),
        'rows': lis,
    }
    return JsonResponse(data)

def subscriptionredemptionmonth(request):

    from app.models import SubscriptionRedemption
    fund = request.GET.get('fund', 0)
    year = request.GET.get('year', 0)
    month = request.GET.get('month', 0)

    queryset = SubscriptionRedemption.objects.select_related('client').filter(fund=fund, trade_date__year=year, \
            trade_date__month=month)
    lis = []
    for row in queryset:
        dic = {
            'client': row.client.first_name + ' ' + row.client.last_name,
            'sub_red': row.get_sub_red_display(),
            'percent_released': row.get_percent_released_display(),
            'trade_date': str(row.trade_date),
            'no_of_units': row.no_of_units,
            'nav': row.nav


        }
        lis.append(dic)

    columns = ['client', ['sub_red', 'Sub. or Red.'], 'trade_date',
               ['no_of_units', 'No. of Units'], ['nav', 'NAV of Trance'],
               'percent_released']
    data = {
        'metaData': {'sorting': 'name'},
        'columns': set_columns(request, column),
        'rows': lis,
    }
    return JsonResponse(data)

def fundsubredtable(request):

    from app.models import FundPerfMonth
    fund = request.GET.get('fund', 0)
    year = request.GET.get('year', 0)
    month = request.GET.get('month', 0)
    fund = FundPerfMonth.objects.filter(fund=fund, value_date__year=year, \
            value_date__month=month).latest('value_date')
    lis = [{
            'summary': 'Previous NAV',
            'euro': fund.previous_nav,
        }, {
            'summary': 'Subscription Amount',
            'euro': fund.subscription_amount,
        }, {
            'summary': 'Redemption Amount',
            'euro': fund.redemption_amount,
        }, {
            'summary': 'Net Movements',
            'euro': fund.net_movement,
        }, {
            'summary': 'Gross Assets After Subs Reds ',
            'euro': fund.gross_assets_after_subs_red ,
        }

    ]

    columns = ['summary','euro']
    data = {
        'columns': set_columns(request, columns),
        'rows': lis
    }
    return JsonResponse(data)

def fundnavreconciliation(request):

    from app.models import FundPerfMonth
    fund = request.GET.get('fund', 0)
    fund = FundPerfMonth.objects.filter(fund=fund).latest('value_date')

    lis = [{
        'euro_nav': fund.euro_nav,
        'no_of_units': fund.no_of_units,
        'euro_nav_fund': fund.euro_nav_fund,
        'no_of_units_fund': fund.no_of_units_fund,

    }]

    columns = {
        'text': 'Valuation From Clients',
        'columns': [{
            'text'     : 'Euro NAV',
            'width'    : 75,
            'dataIndex': 'euro_nav'
        }, {
            'text'     : 'No. of Units',
            'width'    : 75,
            'dataIndex': 'no_of_units'
        }]
    }, {
        'text': '',
    }, {
        'text': 'Valuation From Fund',
        'columns': [{
            'text'     : 'Euro NAV',
            'width'    : 75,
            'dataIndex': 'euro_nav_fund'
        }, {
            'text'     : 'No. of Units',
            'width'    : 75,
            'dataIndex': 'no_of_units_fund'
        }]

    }

    data = {
        'columns': columns,
        'rows': lis
    }
    return JsonResponse(data)

def fundgrossasset(request):

    from app.models import FundPerfMonth, Client

    fund = request.GET.get('fund', 0)
    year = request.GET.get('year', 0)

    qs = FundPerfMonth.objects.filter(fund=fund, value_date__year=year)

    fields = []
    columns = [['type', '']] + get_month_list()

    def set_fields(field, group):
        field_name = field.replace('_', ' ').title()
        dic = {'type': field_name, 'group': group}
        for row in qs:
            month_name = calendar.month_abbr[row.value_date.month]
            dic[month_name.lower()] = getattr(row, field)
        fields.append(dic)

    dic = {
        'previous_nav': 'NAV',
        'performance_fees_added_back': 'NAV',
        'subscription_amount': 'NAV',
        'redemption_amount': 'NAV',
        'net_movement': 'NAV',
        'gross_assets_after_subs_red': 'NAV',

        'nav_securities': 'Assets',
        'nav_securities_total': 'Assets',
        'nav_cash': 'Assets',
        'nav_other_assets': 'Assets',

        'administration_fees': 'Liabilities',
        'audit_fees': 'Liabilities',
        'capital_payable': 'Liabilities',
        'corporate_secretarial_fees': 'Liabilities',
        'custodian_fees': 'Liabilities',
        'financial_statement_prep_fees': 'Liabilities',
        'sub_advisory_fees': 'Liabilities',
        'management_fees': 'Liabilities',
        'performance_fees': 'Liabilities',
        'other_liabilities': 'Liabilities',
        'total_liabilities': 'Liabilities',
    }
    for field, group in dic.iteritems():
        set_fields(field, group)

    data = {
        'metaData': {'sorting': 'name'},
        'columns': set_columns(request, columns),
        'rows': fields,
    }

    return JsonResponse(data)

