from django.contrib import admin
from django.contrib.admin import ModelAdmin

from adminsortable2.admin import SortableAdminMixin

from .models import Offer


class OfferAdmin(SortableAdminMixin, ModelAdmin):
    pass


admin.site.register(Offer, OfferAdmin)
