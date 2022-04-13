from django.contrib import admin

from .models import InviteOrder, TelethonAccount


admin.site.register(TelethonAccount)
admin.site.register(InviteOrder)
