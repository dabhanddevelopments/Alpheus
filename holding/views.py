from django.contrib.auth.decorators import login_required
from alpheus.utils import JsonResponse, set_columns
from holding.models import Holding, HoldingHistory
from comparative.models import Benchmark, BenchmarkHistory
from datetime import date

@login_required
def correlation(request):

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



# W78 (blatant copy and paste from W16) - Line Graph & Bar Chart
# http://localhost:8000/api/holding-performance-benchmark/?fund=2&fields=mtd&format=json
@login_required
def performancebenchmark(request):

    holding = request.GET.get('holding', 0)
    fields = request.GET.get("fields", 0)

    from comparative.models import BenchmarkHistory
    from time import mktime

    objects = BenchmarkHistory.months.select_related('benchmark') \
            .filter(benchmark__holding=holding).only('id', 'value_date', 'benchmark__name', fields)

    # benchmarks
    # TODO: redo this
    dic = {}
    for row in objects:
        date = int(mktime(row.value_date.timetuple())) * 1000
        output = [int(date), row.mtd]
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

    # holdings
    holdings = HoldingHistory.months.select_related('holding') \
             .filter(holding=holding).only('id', 'holding__name', 'value_date', fields)

    from time import mktime

    dic = {}
    for row in holdings:
        date = int(mktime(row.value_date.timetuple())) * 1000
        output = [int(date), float(getattr(row, fields))]
        holding_id = int(row.holding.id)

        try:
            dic[holding_id]['name'] = row.holding.name
        except:
            dic[holding_id] = {}
            dic[holding_id]['name'] = row.holding.name
        try:
            dic[holding_id]['data'].append(output)
        except:
            dic[holding_id]['data'] = []
            dic[holding_id]['data'].append(output)

    for key, val in dic.iteritems():
        response_list.append(val)

    return JsonResponse({'objects': response_list})


# W19 Holding Return Table
# http://localhost:8000/api/holding-returns/?format=json&holding=2
# @TODO: Revise this resource
@login_required
def returns(request):

    holding = request.GET.get('holding', 0)

    # Last month of year is the yearly value
    holdings = HoldingHistory.months.select_related('holding') \
                .filter(value_date__month=12, holding=holding)\
                .only('ann_return1', 'ann_volatility1', 'sharpe_ratio1', \
                                    'value_date', 'mtd', 'holding__name')
    benchmarks = BenchmarkHistory.months.select_related('benchmark') \
                        .filter(value_date__month=12, benchmark__holding=holding) \
                        .only('mtd', 'benchmark__name')
    dic = {}

    # holdings
    holding_column = ['year']
    for year in range(1970, date.today().year + 1):
        dic[year] = {}
        for row in holdings:
            if year == row.value_date.year:
                dic[year]['ann_return1'] = row.ann_return1
                dic[year]['ann_volatility1'] = row.ann_volatility1
                dic[year]['sharpe_ratio1'] = row.sharpe_ratio1
                dic[year][row.holding.name] = row.mtd  # change to: ytd
                if row.holding.name not in holding_column:
                    holding_column.append(row.holding.name)
    # benchmarks
    bench_columns = []
    for year in range(1970, date.today().year + 1):
        for row in benchmarks:
            if year == row.value_date.year:
                dic[year][row.benchmark.name] = row.mtd # change to: ytd
                if row.benchmark.name not in bench_columns:
                    bench_columns.append(row.benchmark.name)

    # sort the bench columns by name
    columns = holding_column + sorted(bench_columns) + ['ann_return1', \
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

    holding = request.GET.get('holding', 0)

    columns = ['best_worst_months']
    positive = {'best_worst_months': 'Positive Months'}
    lis = []

    """ Number of months that are positive """

    # Positive Holding Months
    f = HoldingHistory.months.select_related('holding') \
                    .filter(value_date__month=12, holding=holding) \
                    .only('holding__name', 'mtd')
    p = f.filter(mtd__gt=0)
    holding_name = f.values('holding__name')[0]['holding__name']
    positive[holding_name] = p.count() / f.count() * 100
    columns.append(holding_name)

    # Positive Benchmark Months
    b = BenchmarkHistory.months.filter(value_date__month=12,
                             benchmark__holding=holding) \
                            .values('benchmark__name', 'benchmark__id') \
                            .annotate(count=Count('value_date')) \
                            .order_by('benchmark__name')
    b2 = b.filter(mtd__gt=0)

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
    holdings = HoldingHistory.months.filter(value_date__month=12, holding=holding) \
                            .values('holding__name') \
                            .annotate(Max('mtd'), Min('mtd'),
                                Min('drawdown')) \
                            .order_by('holding__name')
    for row in holdings:
        best[row['holding__name']] = row['mtd__max']
        worst[row['holding__name']] = row['mtd__min']
        drawdown[row['holding__name']] = row['drawdown__min']

    benchmarks = BenchmarkHistory.months.filter(
                         value_date__month=12, benchmark__holding=holding) \
                                .values('benchmark__name') \
                                .annotate(Max('mtd'), Min('mtd'),
                                    Min('drawdown')) \
                                .order_by('benchmark__name')
    for bench in benchmarks:
        best[bench['benchmark__name']] = bench['mtd__max']
        worst[bench['benchmark__name']] = bench['mtd__min']
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

    holding_id = request.GET.get('holding', 0)

    lis = []
    columns = ['+10%', '5 to 10%', '4%', '3%', '2%', '1%', '0%',
                   '-1%', '-2%', '-3%', '-4%', '-5 to 10%', '-10%']

    holdings = HoldingHistory.months.filter(holding=holding_id)

    # get 10+
    count = holdings.filter(mtd__gte=10).aggregate(Count('mtd'))
    lis.append([columns[0], count['mtd__count']])

    # get 5 to 10
    count = holdings.filter(mtd__gte=5, mtd__lt=10) \
                                        .aggregate(Count('mtd'))
    lis.append([columns[1], count['mtd__count']])

    # get -5 to +5
    # @TODO: On MSSQL SIGNED is called INT
    sql = """
    SELECT id,
        Cast(mtd as SIGNED) as mtd,
        Count(mtd) as count
    FROM holding_holdinghistory
    WHERE holding_id = %s
        AND mtd > -5 AND mtd < 5
    GROUP BY Cast(mtd as SIGNED)
    ORDER BY mtd DESC;
    """
    raw = HoldingHistory.months.raw(sql, [holding_id])
    dic = {}
    for holding in raw:
        dic[str(holding.mtd)] = holding.count
    for index in range(4, -5, -1):
        try:
            count = dic[str(index)]
            print count
        except:
            count = 0
        lis.append([str(index) + '%', count])

    # get -5 to -10
    count = holdings.filter(mtd__gte=5, mtd__lt=10).aggregate(Count('mtd'))
    lis.append([columns[11], count['mtd__count']])

    # get -10 and Lower
    count = holdings.filter(mtd__gte=10).aggregate(Count('mtd'))
    lis.append([columns[12], count['mtd__count']])

    dic = {
        'columns': columns,
        'objects': [{'data': lis}]
    }
    return JsonResponse(dic)


@login_required
def correlation(request):

    holding_id = request.GET.get('holding', 0)

    # Get the latest values
    holding = HoldingHistory.months.select_related('holding').filter(holding=holding_id) \
                                        .latest('value_date')
    benchmarks = Benchmark.objects.filter(holding=holding_id)

    columns = ['Correlation Matrix', holding.holding.name]
    lis = []
    dic = {}

    # holding correlation
    dic['Correlation Matrix'] = holding.holding.name
    dic[holding.holding.name] = holding.mtd / holding.mtd
    for bench in benchmarks:
        dic[bench.name] = holding.mtd / bench.mtd
    lis.append(dic)

    # benchmark correlation
    for col in benchmarks:
        dic = {}
        for row in benchmarks:
            dic[row.name] = row.mtd / col.mtd
        dic['Correlation Matrix'] = col.name
        dic[holding.holding.name] = holding.mtd / col.mtd
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

    holding_id = request.GET.get('holding', 0)

    holdings = HoldingHistory.months.filter(holding=holding_id) \
                                    .values('holding__name') \
                                    .annotate(Avg('mtd')) \
                                    .order_by('holding__name')[0]
    dic = {
        holdings['holding__name']: holdings['mtd__avg'],
    }

    benchmarks = BenchmarkHistory.months.filter(benchmark__holding=holding_id,
                                     mtd__gt=0) \
                                    .values('benchmark__name') \
                                    .annotate(Avg('mtd')) \
                                    .order_by('benchmark__name')
    for bench in benchmarks:
        dic[bench['benchmark__name']] = bench['mtd__avg']

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

