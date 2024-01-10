from django.contrib import admin

from .models import States, LGA, Ward, PollingUnit

admin.site.register(States)
admin.site.register(LGA)
admin.site.register(Ward)
admin.site.register(PollingUnit)
