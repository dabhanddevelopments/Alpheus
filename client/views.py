from django.contrib.auth.decorators import login_required
from client.models import ClientHistory
from comparative.models import Benchmark, BenchmarkHistory
from time import mktime
from alpheus.utils import JsonResponse, set_columns
from datetime import date
import calendar


@login_required
def returns(request):

    client = request.GET.get('client', 0)

    # Last month of year is the yearly value
    clients = ClientHistory.months.select_related('client') \
                .filter(value_date__month=12, client=client)\
                .only('ann_return1', 'ann_volatility1', 'sharpe_ratio1', \
                                    'value_date', 'performance', 'client__first_name', 'client__last_name')
    benchmarks = BenchmarkHistory.months.select_related('benchmark') \
                        .filter(value_date__month=12, benchmark__client=client) \
                        .only('performance', 'benchmark__name')
    dic = {}

    # clients
    client_column = ['year']
    for year in range(1970, date.today().year + 1):
        dic[year] = {}
        for row in clients:
            if year == row.value_date.year:
                dic[year]['ann_return1'] = row.ann_return1
                dic[year]['ann_volatility1'] = row.ann_volatility1
                dic[year]['sharpe_ratio1'] = row.sharpe_ratio1
                dic[year][row.client.name()] = row.performance  # change to: ytd
                if row.client.name() not in client_column:
                    client_column.append(row.client.name())
    # benchmarks
    bench_columns = []
    for year in range(1970, date.today().year + 1):
        for row in benchmarks:
            if year == row.value_date.year:
                dic[year][row.benchmark.name] = row.performance # change to: ytd
                if row.benchmark.name not in bench_columns:
                    bench_columns.append(row.benchmark.name)

    # sort the bench columns by name
    columns = client_column + sorted(bench_columns) + ['ann_return1', \
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

    client = request.GET.get('client', 0)

    columns = ['best_worst_months']
    positive = {'best_worst_months': 'Positive Months'}
    lis = []

    """ Number of months that are positive """

    # Positive Client Months
    f = ClientHistory.months.select_related('client') \
                    .filter(value_date__month=12, client=client) \
                    .only('performance', 'client__first_name', 'client__last_name')
    p = f.filter(performance__gt=0)
    client_name = str(f[0].client).replace(', ', '_').lower()
    positive[client_name] = p.count() / f.count() * 100
    columns.append(client_name)

    # Positive Benchmark Months
    b = BenchmarkHistory.months.filter(value_date__month=12,
                             benchmark__client=client) \
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
    clients = ClientHistory.months.filter(value_date__month=12, client=client) \
                            .values('client__last_name', 'client__first_name') \
                            .annotate(Max('performance'), Min('performance'),
                                Min('drawdown')) \
                            .order_by('client__last_name', 'client__first_name')


    for row in clients:
        client_name = ' '.join([row['client__last_name'], row['client__first_name']])
        best[client_name] = row['performance__max']
        worst[client_name] = row['performance__min']
        drawdown[client_name] = row['drawdown__min']

    benchmarks = BenchmarkHistory.months.filter(
                         value_date__month=12, benchmark__client=client) \
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

    client_id = request.GET.get('client', 0)

    lis = []
    columns = ['+10%', '5 to 10%', '4%', '3%', '2%', '1%', '0%',
                   '-1%', '-2%', '-3%', '-4%', '-5 to 10%', '-10%']

    clients = ClientHistory.months.filter(client=client_id)

    # get 10+
    count = clients.filter(performance__gte=10).aggregate(Count('performance'))
    lis.append([columns[0], count['performance__count']])

    # get 5 to 10
    count = clients.filter(performance__gte=5, performance__lt=10) \
                                        .aggregate(Count('performance'))
    lis.append([columns[1], count['performance__count']])

    # get -5 to +5
    # @TODO: On MSSQL SIGNED is called INT
    sql = """
    SELECT id,
        Cast(performance as SIGNED) as performance,
        Count(performance) as count
    FROM client_clienthistory
    WHERE client_id = %s
        AND performance > -5 AND performance < 5
    GROUP BY Cast(performance as SIGNED)
    ORDER BY performance DESC;
    """
    raw = ClientHistory.months.raw(sql, [client_id])
    dic = {}
    for client in raw:
        dic[str(client.performance)] = client.count
    for index in range(4, -5, -1):
        try:
            count = dic[str(index)]
            print count
        except:
            count = 0
        lis.append([str(index) + '%', count])

    # get -5 to -10
    count = clients.filter(performance__gte=5, performance__lt=10).aggregate(Count('performance'))
    lis.append([columns[11], count['performance__count']])

    # get -10 and Lower
    count = clients.filter(performance__gte=10).aggregate(Count('performance'))
    lis.append([columns[12], count['performance__count']])

    dic = {
        'columns': columns,
        'objects': [{'data': lis}]
    }
    return JsonResponse(dic)


@login_required
def correlation(request):

    client_id = request.GET.get('client', 0)

    # Get the latest values
    client = ClientHistory.months.select_related('client').filter(client=client_id) \
                                        .latest('value_date')
    benchmarks = Benchmark.objects.filter(client=client_id)

    columns = ['Correlation Matrix', client.client.name()]
    lis = []
    dic = {}

    # client correlation
    dic['Correlation Matrix'] = client.client.name()
    dic[client.client.name()] = client.performance / client.performance
    for bench in benchmarks:
        dic[bench.name] = client.performance / bench.performance
    lis.append(dic)

    # benchmark correlation
    for col in benchmarks:
        dic = {}
        for row in benchmarks:
            dic[row.name] = row.performance / col.performance
        dic['Correlation Matrix'] = col.name
        dic[client.client.name] = client.performance / col.performance
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

    client_id = request.GET.get('client', 0)

    clients = ClientHistory.months.filter(client=client_id) \
                                    .values('client__first_name', 'client__last_name') \
                                    .annotate(Avg('performance')) \
                                    .order_by('client__last_name', 'client__first_name')[0]
    client_name = '_'.join([clients['client__last_name'], clients['client__first_name']]).lower()
    dic = {
        client_name: clients['performance__avg'],
    }

    benchmarks = BenchmarkHistory.months.filter(benchmark__client=client_id,
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

    from client.models import CurrencyPosition, FxHedge, FxRate
    from django.db.models import Sum
    client_id = request.GET.get('client', 0)

    sql = """
        SELECT id, currency_id, amount, settlement_date
        FROM `client_fxhedge`
        WHERE (`client_fxhedge`.`client_id` = %s  AND `client_fxhedge`.`settlement_date` > %s )
        GROUP BY `client_fxhedge`.`currency_id`
        ORDER BY `client_fxhedge`.`settlement_date` ASC
    """
    fx = FxHedge.objects.raw(sql, [client_id, date.today()])
    lis = []
    for row in fx:
       perf = CurrencyPosition.objects.select_related('currency') \
                        .filter(client=client_id, currency=row.currency_id) \
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

    client = request.GET.get('client', 0)
    year = request.GET.get('year', 0)
    month = request.GET.get('month', 0)
    client = ClientHistory.months.filter(client=client, value_date__year=year, \
            value_date__month=month).latest('value_date')
    lis = [{
            'summary': 'Previous NAV',
            'euro': client.previous_nav,
        }, {
            'summary': 'Subscription Amount',
            'euro': client.subscription_amount,
        }, {
            'summary': 'Redemption Amount',
            'euro': client.redemption_amount,
        }, {
            'summary': 'Net Movements',
            'euro': client.net_movement,
        }, {
            'summary': 'Gross Assets After Subs Reds ',
            'euro': client.gross_assets_after_subs_red ,
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

    client = request.GET.get('client', 0)
    client = ClientHistory.months.filter(client=client).latest('value_date')

    lis = [{
        'euro_nav_client': client.euro_nav_client,
        'no_of_units': client.no_of_units,
        'euro_nav_client': client.euro_nav_client,
        'no_of_units_client': client.no_of_units_client,

    }]

    columns = {
        'text': 'Valuation From Clients',
        'columns': [{
            'text'     : 'Euro NAV',
            'width'    : 75,
            'dataIndex': 'euro_nav_client'
        }, {
            'text'     : 'No. of Units',
            'width'    : 75,
            'dataIndex': 'no_of_units'
        }]
    }, {
        'text': '',
    }, {
        'text': 'Valuation From Client',
        'columns': [{
            'text'     : 'Euro NAV',
            'width'    : 75,
            'dataIndex': 'euro_nav_client'
        }, {
            'text'     : 'No. of Units',
            'width'    : 75,
            'dataIndex': 'no_of_units_client'
        }]

    }

    data = {
        'columns': columns,
        'rows': lis
    }
    return JsonResponse(data)




# W16 - Line Graph & Bar Chart
# http://localhost:8000/api/client-performance-benchmark/?client=2&fields=performance&format=json
@login_required
def performancebenchmark(request):

    client = request.GET.get('client', 0)
    fields = request.GET.get("fields", 0)

    objects = BenchmarkHistory.months.select_related('benchmark') \
            .filter(benchmark__client=client).only('id', 'value_date', 'benchmark__name', fields)

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

    # clients
    clients = ClientHistory.months.select_related('client') \
             .filter(client=client, fund__isnull=True).only('id', 'client__first_name', 'client__last_name', 'value_date', fields)

    dic = {}
    for row in clients:
        date = int(mktime(row.value_date.timetuple())) * 1000
        output = [int(date), getattr(row, fields)]
        client_id = int(row.client.id)

        try:
            dic[client_id]['name'] = row.client.name()
        except:
            dic[client_id] = {}
            dic[client_id]['name'] = row.client.name()
        try:
            dic[client_id]['data'].append(output)
        except:
            dic[client_id]['data'] = []
            dic[client_id]['data'].append(output)

    for key, val in dic.iteritems():
        response_list.append(val)

    return JsonResponse({'objects': response_list})

