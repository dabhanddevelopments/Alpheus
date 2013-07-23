from django.contrib.auth.decorators import login_required
from fund.models import FundHistory
from comparative.models import Benchmark, BenchmarkHistory
from time import mktime
from alpheus.utils import JsonResponse, set_columns
from datetime import date
import calendar

def get_month_list():
    months = []
    for month in range(1, 13):
        months.append(calendar.month_abbr[month].lower())
    return months








# W16 - Line Graph & Bar Chart
# http://localhost:8000/api/fund-performance-benchmark/?fund=2&fields=performance&format=json
@login_required
def performancebenchmark(request):

    fund = request.GET.get('fund', 0)
    fields = request.GET.get("fields", 0)

    objects = BenchmarkHistory.months.select_related('benchmark') \
            .filter(benchmark__fund=fund).only('id', 'value_date', 'benchmark__name', fields)

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
    funds = FundHistory.months.select_related('fund') \
             .filter(fund=fund).only('id', 'fund__name', 'value_date', fields)

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
        response_list.append(val)

    return JsonResponse({'objects': response_list})

# W19 Fund Return Table
# http://localhost:8000/api/fund-returns/?format=json&fund=2
# @TODO: Revise this resource
@login_required
def returns(request):

    fund = request.GET.get('fund', 0)

    # Last month of year is the yearly value
    funds = FundHistory.months.select_related('fund') \
                .filter(value_date__month=12, fund=fund)\
                .only('ann_return1', 'ann_volatility1', 'sharpe_ratio1', \
                                    'value_date', 'performance', 'fund__name')
    benchmarks = BenchmarkHistory.months.select_related('benchmark') \
                        .filter(value_date__month=12, benchmark__fund=fund) \
                        .only('performance', 'benchmark__name')
    dic = {}

    # funds
    fund_column = ['year']
    for year in range(1970, date.today().year + 1):
        dic[year] = {}
        for row in funds:
            if year == row.value_date.year:
                dic[year]['ann_return1'] = row.ann_return1
                dic[year]['ann_volatility1'] = row.ann_volatility1
                dic[year]['sharpe_ratio1'] = row.sharpe_ratio1
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
    columns = fund_column + sorted(bench_columns) + ['ann_return1', \
                                    'ann_volatility1', 'sharpe_ratio1']

    result = []
    for key, val in dic.iteritems():
        if val:
            val['year'] = key
            result.append(val)

    from operator import itemgetter
    
    dic = {
        'metaData': {'sorting': 'year'},
        'columns': set_columns(request, columns),
        'rows': sorted(result, key=itemgetter('year'), reverse=True),
    }
    return JsonResponse(dic)

@login_required
def bestworst(request):

    from django.db.models import Max, Min, Avg, Count

    fund = request.GET.get('fund', 0)

    columns = ['best_worst_months']
    positive = {'best_worst_months': 'Positive Months'}
    lis = []

    """ Number of months that are positive """

    # Positive Fund Months
    f = FundHistory.months.select_related('fund') \
                    .filter(value_date__month=12, fund=fund) \
                    .only('fund__name', 'performance')
    p = f.filter(performance__gt=0)
    fund_name = f.values('fund__name')[0]['fund__name']
    positive[fund_name] = p.count() / f.count() * 100
    columns.append(fund_name)

    # Positive Benchmark Months
    b = BenchmarkHistory.months.filter(value_date__month=12,
                             benchmark__fund=fund) \
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
    funds = FundHistory.months.filter(value_date__month=12, fund=fund) \
                            .values('fund__name') \
                            .annotate(Max('performance'), Min('performance'),
                                Min('drawdown')) \
                            .order_by('fund__name')
    for row in funds:
        best[row['fund__name']] = row['performance__max']
        worst[row['fund__name']] = row['performance__min']
        drawdown[row['fund__name']] = row['drawdown__min']

    benchmarks = BenchmarkHistory.months.filter(
                         value_date__month=12, benchmark__fund=fund) \
                                .values('benchmark__name') \
                                .annotate(Max('performance'), Min('performance'),
                                    Min('drawdown')) \
                                .order_by('benchmark__name')
    for bench in benchmarks:
        best[bench['benchmark__name']] = bench['performance__max']
        worst[bench['benchmark__name']] = bench['performance__min']
        drawdown[bench['benchmark__name']] = bench['drawdown__min']
    lis.append(best)
    lis.append(worst)
    lis.append(drawdown)

    dic = {
        'metaData': {'sorting': 'year'},
        'columns': set_columns(request, columns),
        'rows': lis,
    }
    return JsonResponse(dic)


@login_required
def returnhistogram(request):

    from django.db.models import Count

    fund_id = request.GET.get('fund', 0)

    lis = []
    columns = ['+10%', '5 to 10%', '4%', '3%', '2%', '1%', '0%',
                   '-1%', '-2%', '-3%', '-4%', '-5 to 10%', '-10%']

    funds = FundHistory.months.filter(fund=fund_id)

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
    FROM fund_fundhistory
    WHERE fund_id = %s
        AND performance > -5 AND performance < 5
    GROUP BY Cast(performance as SIGNED)
    ORDER BY performance DESC;
    """
    raw = FundHistory.months.raw(sql, [fund_id])
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


@login_required
def correlation(request):

    fund_id = request.GET.get('fund', 0)

    # Get the latest values
    fund = FundHistory.months.select_related('fund').filter(fund=fund_id) \
                                        .latest('value_date')
    benchmarks = Benchmark.objects.filter(fund=fund_id)

    columns = ['Correlation Matrix', fund.fund.name]
    lis = []
    dic = {}

    # fund correlation
    dic['Correlation Matrix'] = fund.fund.name
    dic[fund.fund.name] = fund.performance / fund.performance
    for bench in benchmarks:
        dic[bench.name] = fund.performance / bench.performance
    lis.append(dic)

    # benchmark correlation
    for col in benchmarks:
        dic = {}
        for row in benchmarks:
            dic[row.name] = row.performance / col.performance
        dic['Correlation Matrix'] = col.name
        dic[fund.fund.name] = fund.performance / col.performance
        lis.append(dic)
        columns.append(col.name)

    dic = {
        'columns': set_columns(request, columns),
        'rows': lis
    }
    return JsonResponse(dic)


@login_required
def negativemonths(request):

    from django.db.models import Avg

    fund_id = request.GET.get('fund', 0)

    funds = FundHistory.months.filter(fund=fund_id) \
                                    .values('fund__name') \
                                    .annotate(Avg('performance')) \
                                    .order_by('fund__name')[0]
    dic = {
        funds['fund__name']: funds['performance__avg'],
    }

    benchmarks = BenchmarkHistory.months.filter(benchmark__fund=fund_id,
                                     performance__gt=0) \
                                    .values('benchmark__name') \
                                    .annotate(Avg('performance')) \
                                    .order_by('benchmark__name')
    for bench in benchmarks:
        dic[bench['benchmark__name']] = bench['performance__avg']

    columns = [key for key, val in dic.iteritems()]

    return dic, columns

@login_required
def negativemonthstable(request):

    dic, columns = negativemonths(request)
    avg_perf = 'Avg Performance in neg months'
    dic[avg_perf] = 'Avg Performance'
    columns = [avg_perf] + columns

    data = {
        'columns': set_columns(request, columns),
        'rows': [dic]
    }
    return JsonResponse(data)

@login_required
def negativemonthsgraph(request):

    dic, columns = negativemonths(request)
    lis = [[key, val] for key, val in dic.iteritems()]

    data = {
        'columns': columns,
        'objects': [{'data': lis}]
    }
    return JsonResponse(data)

@login_required
def currencyhedge(request):

    from fund.models import CurrencyPosition, FxHedge, FxRate
    from django.db.models import Sum
    fund_id = request.GET.get('fund', 0)

    sql = """
        SELECT id, currency_id, amount, settlement_date
        FROM `fund_fxhedge`
        WHERE (`fund_fxhedge`.`fund_id` = %s  AND `fund_fxhedge`.`settlement_date` > %s )
        GROUP BY `fund_fxhedge`.`currency_id`
        ORDER BY `fund_fxhedge`.`settlement_date` ASC
    """
    fx = FxHedge.objects.raw(sql, [fund_id, date.today()])
    lis = []
    for row in fx:
       perf = CurrencyPosition.objects.select_related('currency') \
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



@login_required
def subredtable(request):

    fund = request.GET.get('fund', 0)
    year = request.GET.get('year', 0)
    month = request.GET.get('month', 0)
    fund = FundHistory.months.filter(fund=fund, value_date__year=year, \
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

@login_required
def reconciliation(request):

    fund = request.GET.get('fund', 0)
    fund = FundHistory.months.filter(fund=fund).latest('value_date')

    lis = [{
        'euro_nav_fund': fund.euro_nav_fund,
        'no_of_units': fund.no_of_units,
        'euro_nav_fund': fund.euro_nav_fund,
        'no_of_units_fund': fund.no_of_units_fund,

    }]

    columns = {
        'text': 'Valuation From Clients',
        'columns': [{
            'text'     : 'Euro NAV',
            'width'    : 75,
            'dataIndex': 'euro_nav_fund'
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

@login_required
def grossasset(request, grid):

    from fund.models import FundHistory
    from client.models import Client
    
    columns = [field for field, group in grid.iteritems()]
    columns.append('value_date')

    fund = request.GET.get('fund', 0)
    year = request.GET.get('year', 0)

    qs = FundHistory.months.filter(fund=fund, value_date__year=year).only(*columns)
    
    fields = []
    columns = [['type', '']] + get_month_list()

    def set_fields(field, group):
        field_name = field.replace('_', ' ').title()
        dic = {'type': field_name, 'group': group}
        for row in qs:
            month_name = calendar.month_abbr[row.value_date.month]
            dic[month_name.lower()] = getattr(row, field)
        fields.append(dic)

    for field, group in grid.iteritems():
        set_fields(field, group)

    data = {
        'metaData': {'sorting': 'name'},
        'columns': set_columns(request, columns),
        'rows': fields,
    }

    return JsonResponse(data)

# W13
@login_required
def grossasset1(request):
    grid = {
        'previous_nav': 'NAV',
        'euro_nav_fund': 'NAV',
        'subscription_amount': 'NAV',
        'redemption_amount': 'NAV',
        'performance_fee_added_back': 'NAV',
        'gross_assets_after_subs_red': 'NAV',

        'nav_securities': 'Assets',
        'nav_cash': 'Assets',
        'nav_other_assets': 'Assets',
        'nav_securities_total': 'Assets',

        'administrator_fee_payable': 'Liabilities & Fees',
        'auditor_fee_payable': 'Liabilities',
        'capital_fee_payable': 'Liabilities',
        'corporate_secretarial_payable': 'Liabilities',
        'custodian_fee_payable': 'Liabilities',
        'financial_statement_prep_payable': 'Liabilities',
        'sub_advisory_fee_payable': 'Liabilities',
        'management_fee_payable': 'Liabilities',
        'performance_fee_payable': 'Liabilities',
        'other_liabilities_payable': 'Liabilities',
        'total_liabilities_payable': 'Liabilities',
        'assets_liabilities': 'Liabilities',
    }
    return grossasset(request, grid)

# W13b
@login_required
def grossasset2(request):
    grid = {
        'euro_nav_fund': 'NAV',
        'net_movement': 'NAV',
        'subscription_amount': 'NAV',
        'redemption_amount': 'NAV',
        'gross_assets_after_subs_red': 'NAV',
        'performance_fee_added_back': 'NAV',

        'long_portfolio': 'Assets',
        'nav_cash': 'Assets',
        'fet_valuation': 'Assets',
        'accrued_interest': 'Assets',
        'interest_receivable_on_banks': 'Assets',
        'dividends_receivable': 'Assets',
        'recv_for_transactions': 'Assets',
        'nav_securities_total': 'Assets',

        'transaction_fee_payable': 'Liabilities',
        'management_fee_payable': 'Liabilities',
        'serv_act_fee_payable': 'Liabilities',
        'trustee_fee_payable': 'Liabilities',   #column did not exist
        'auditor_fee_payable': 'Liabilities',
        'performance_fee_payable': 'Liabilities',
        'other_liabilities_payable': 'Liabilities', 
        'total_liabilities': 'Liabilities',
        'assets_liabilities': 'Liabilities',
    }
    return grossasset(request, grid)

# W13c
@login_required
def grossasset3(request):
    grid = {
        'euro_nav_fund': 'NAV',
        'net_movement': 'NAV',
        'subscription_amount': 'NAV',
        'redemption_amount': 'NAV',
        'gross_assets_after_subs_red': 'NAV',
        'performance_fee_added_back': 'NAV',

        'nav_securities': 'Assets',
        'put_options': 'Assets',  #column did not exist
        'call_options': 'Assets',  #column did not exist
        'financial_futures': 'Assets',  #column did not exist
        'nav_cash': 'Assets',
        'fet_valuation': 'Assets',
        'dividends_receivable': 'Assets',
        'interest_receivable_on_banks': 'Assets',
        #'accrued_interest': 'Assets', # not clear if this should be here
        'nav_securities_total': 'Assets',

        'transaction_fee_payable': 'Liabilities',
        'management_fee_payable': 'Liabilities',
        'serv_act_fee_payable': 'Liabilities',
        'trustee_fee_payable': 'Liabilities',
        'auditor_fee_payable': 'Liabilities',
        'performance_fee_payable': 'Liabilities',
        'other_liabilities_payable': 'Liabilities',
        'total_liabilities_payable  ': 'Liabilities',
        'assets_liabilities': 'Liabilities',
    }
    return grossasset(request, grid)

#W13d
@login_required
def grossasset4(request):
    grid = {
        'euro_nav': 'NAV',
        'net_movement': 'NAV',
        'subscription_amount': 'NAV',
        'redemption_amount': 'NAV',
        'gross_assets_after_subs_red': 'NAV',
        'performance_fee_added_back': 'NAV',


        'long_portfolio': 'Assets',
        'nav_cash': 'Assets',
        'receivables': 'Assets',  #column did not exist
        'prepaid_or_recov_amounts': 'Assets',  #column did not exist
        'financial_futures': 'Assets',
        'transitory_assets': 'Assets',  #column did not exist

        'nav_securities_total': 'Liabilities',  #column did not exist
        'transaction_fee_payable': 'Liabilities',
        'management_fee_payable': 'Liabilities',
        'serv_act_fee_payable': 'Liabilities',
        'trustee_fee_payable': 'Liabilities',
        'auditor_fee_payable': 'Liabilities',
        'performance_fee_payable': 'Liabilities',
        'other_liabilities_payable': 'Liabilities',
        'total_liabilities_payable': 'Liabilities',
        'assets_liabilities': 'Liabilities',
    }
    return grossasset(request, grid)

#W13e
@login_required
def grossasset5(request):
    grid = {
        'euro_nav': 'NAV',
        'net_movement': 'NAV',
        'subscription_amount': 'NAV',
        'redemption_amount': 'NAV',
        'gross_assets_after_subs_red': 'NAV',
        'performance_fee_added_back': 'NAV',


        'nav_securities': 'Assets',
        'nav_cash': 'Assets',
        'fet_valuation': 'Assets',  #column did not exist
        'interest_receivable_on_banks': 'Assets',  #column did not exist
        'receivables': 'Assets',  #column did not exist
        'prepaid_or_recov_amounts': 'Assets',

        'nav_securities_total': 'Liabilities',  #column did not exist
        'transaction_fee_payable': 'Liabilities',
        'management_fee_payable': 'Liabilities',
        'serv_act_fee_payable': 'Liabilities',
        'trustee_fee_payable': 'Liabilities',
        'auditor_fee_payable': 'Liabilities',
        'performance_fee_payable': 'Liabilities',
        'other_fee': 'Liabilities',
        'total_liabilities_payable': 'Liabilities',
        'assets_liabilities': 'Liabilities',
    }
    return grossasset(request, grid)
