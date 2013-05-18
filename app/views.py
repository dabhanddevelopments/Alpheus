from django.shortcuts import render, render_to_response
from app.models import Menu, Holding, Trade
from django.template import RequestContext
#from django.core.context_processors import csrf
#from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator

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
                            
def month_columns(column_names, width=False):

    # first column is 0, the rest are 1
    if not width:
        width = {}
        width[0] = 50
        width[1] = 50

    columns = []
    for key, column in enumerate(column_names):
        dic = {}
        dic = {
            'dataIndex': column,
            'text': column.title().replace('_', ' '),
        }
        if key == 0:
            dic['width'] = width[0]
        else:
            dic['width'] = width[1]
        columns.append(dic)

    return columns

        
from alpheus.utils import JsonResponse
def holding_table (request):

    fund = request.GET.get('fund', 0)
    
    sql = """
        SELECT * FROM (
            SELECT * FROM app_holding ORDER BY value_date DESC
        ) AS sub 
        WHERE fund_id = %s
        AND name != 'Blackrock US'
        GROUP BY name
    """
    holding = Holding.objects.raw(sql, [fund])
    
    lis = []
    fields = ['name', 'sector', 'sub_sector', 'location','currency', \
                                'no_of_units', 'current_price', 'nav']
    for hold in holding:
        dic = {}
        for field in fields:
            dic[field] = str(getattr(hold, field))
        dic['id'] = str(getattr(hold, 'identifier'))
        lis.append(dic)
        
    columns = month_columns(fields, [80, 80])

    data = {
        'metaData': {'sorting': 'name'},
        'columns': columns,
        'rows': lis,
    }
    return JsonResponse(data)
    
    
def holding_line_graph(request):

    import datetime 
    from time import mktime
    
    identifier = request.GET.get('identifier', 0)
    fund = request.GET.get('fund', 0)

    if not identifier:
        # get first holding in list
        sql = """ 
            SELECT id, identifier FROM (
                SELECT * FROM app_holding WHERE fund_id = %s ORDER BY value_date DESC
            ) AS sub 
            GROUP BY name
        """
        holding = Holding.objects.raw(sql, [fund])
        try: 
            identifier = holding[0].identifier
        except:
            identifier = 0
            
    sql = """
        SELECT id, value_date, current_price  
        FROM app_holding 
        WHERE identifier = %s  
        ORDER BY value_date
    """

    # holdings for line graph 
    holding = Holding.objects.raw(sql, [identifier])
    line_lis = []
    for hold in holding:
        date = int(mktime(hold.value_date.timetuple())) * 1000
        innerlis=[int(str(date)), hold.current_price]
        line_lis.append(innerlis)
          
    # trades for bar graph
    objects = Trade.objects.filter(identifier=identifier)
    bar_lis = []        
    for row in objects:            
        date = int(mktime(row.trade_date.timetuple())) * 1000
        innerlis=[int(str(date)), row.no_of_units]
        bar_lis.append(innerlis)
   
    dic = {
        'line': line_lis,
        'bar': bar_lis,
    }
    return JsonResponse(dic)
