from django.contrib import admin

from .models import Schedule, Statistic, Competition


admin.site.register(Schedule)
admin.site.register(Statistic)
admin.site.register(Competition)
