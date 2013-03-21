from django.shortcuts import render, render_to_response
from app.models import Menu
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



