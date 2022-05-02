from django.contrib import admin

from .models import InviteOrder
from .models import SpamOrder


admin.site.register(InviteOrder)
admin.site.register(SpamOrder)
