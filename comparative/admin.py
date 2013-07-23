from django.contrib import admin
from comparative.models import *

admin.site.register(Benchmark)
admin.site.register(BenchmarkHistory)
admin.site.register(Peer)
admin.site.register(PeerHistory)

