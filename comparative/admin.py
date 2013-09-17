from django.contrib import admin
from comparative.models import *


class BenchmarkAdmin(admin.ModelAdmin):
    fields = ('name', 'benchmark_type', 'bloomberg_code', 'description')


class PeerAdmin(admin.ModelAdmin):
    fields = ('name', 'peer_type', 'bloomberg_code', 'description')


admin.site.register(Benchmark, BenchmarkAdmin)
admin.site.register(BenchmarkHistory)
admin.site.register(Peer, PeerAdmin)
admin.site.register(PeerHistory)

