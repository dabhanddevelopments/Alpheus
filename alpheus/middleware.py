from django.db import connection
from django.template import Template, Context

class SQLLogMiddleware:

    def process_response ( self, request, response ): 

        try:
            request.GET['format']
        except:
            return response

        time = 0.0
        for q in connection.queries:
		    time += float(q['time'])
        
        t = Template('''


Total query count: {{ count }}
Total execution time: {{ time }}
{% for sql in sqllog %}
    {{ sql.time }}: {{ sql.sql }}
{% endfor %}
        ''')

        response.content = "%s%s" % ( response.content, t.render(Context({'sqllog':connection.queries,'count':len(connection.queries),'time':time})))
        return response
