from django.contrib import admin
from .models import Menu, OpeningHour, Table
from django_summernote.admin import SummernoteModelAdmin
import bleach

# Register your models here.


class MenuAdmin(SummernoteModelAdmin):
    summernote_fields = ("name",)
    def name_preview(self, obj):
        return bleach.clean(obj.name, tags=[], strip=True)
    name_preview.short_name = "name (preview)"
    list_display = ("name_preview","description", "price",)
    list_filter = ("categories",)
    search_fields = ("name", "categories")


admin.site.register(Menu, MenuAdmin)


class OpeningHourAdmin(admin.ModelAdmin):
    list_display = ("day_of_week", "open_time", "close_time")
    ordering = ("day_of_week",)


admin.site.register(OpeningHour, OpeningHourAdmin)

class TableAdmin(admin.ModelAdmin):
    list_display = ("table_number", "capacity", "status")
    list_filter = ("status", "capacity",)
    search_fields = ("table_number",)

admin.site.register(Table, TableAdmin)
