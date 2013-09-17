from django.http import HttpResponse
from django.utils import simplejson
from json import encoder
from django.core.serializers.json import DjangoJSONEncoder

class JsonResponse(HttpResponse):
    def __init__(self, data):

        # make sure all Decimals have two decimal places
        from decimal import *
        try:
            for index, row in enumerate(data['rows']):
                for key, val in row.items():
                    if isinstance(val, Decimal) or isinstance(val, float):
                        assert False
                        data['rows'][index][key] = str(Decimal("%.2f" % val))
        except:
            pass

        content = simplejson.dumps(data, indent=2, ensure_ascii=False, cls=DjangoJSONEncoder)
        super(JsonResponse, self).__init__(content=content,
                            mimetype='application/json; charset=utf8')

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


from django.contrib import admin

def create_modeladmin(modeladmin, model, name = None):
    class  Meta:
        proxy = True
        app_label = model._meta.app_label

    attrs = {'__module__': '', 'Meta': Meta}

    newmodel = type(name, (model,), attrs)

    admin.site.register(newmodel, modeladmin)
    return modeladmin


