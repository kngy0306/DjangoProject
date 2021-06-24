from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Airport)
admin.site.register(Passenger)

# 管理アプリケーションをカスタマイズ可能


class FlightAdmin(admin.ModelAdmin):
    list_display = ("id", "origin", "destination", "duration")


# Register your models here.
admin.site.register(Flight, FlightAdmin)
