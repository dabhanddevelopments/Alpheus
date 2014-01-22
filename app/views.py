from django.shortcuts import render, render_to_response
#from app.models import Menu, Holding, Trade
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
    column_border_y = request.GET.get('column_border_y', False)
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



