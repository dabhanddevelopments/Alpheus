from django.http import HttpResponse
from django.utils import simplejson
from json import encoder
encoder.FLOAT_REPR = lambda o: format(o, '.2f')

class JsonResponse(HttpResponse):
    def __init__(self, data):

        # make sure all Decimals have two decimal places
        from decimal import *
        try:
            for index, row in enumerate(data['rows']):
                for key, val in row.items():
                    if isinstance(val, Decimal) or isinstance(val, float):
                        data['rows'][index][key] = str(Decimal("%.2f" % val))
        except:
            pass

        content = simplejson.dumps(data, indent=2, ensure_ascii=False)
        super(JsonResponse, self).__init__(content=content,
                            mimetype='application/json; charset=utf8')
