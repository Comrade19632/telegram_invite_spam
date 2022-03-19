from django.contrib import admin
from django.contrib.admin import ModelAdmin

from adminsortable2.admin import SortableAdminMixin

from .models import Message


class MessageAdmin(SortableAdminMixin, ModelAdmin):
    list_display = ("created", "text")


admin.site.register(Message, MessageAdmin)
