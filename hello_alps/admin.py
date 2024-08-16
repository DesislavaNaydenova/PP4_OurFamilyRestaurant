from django.contrib import admin
from .models import Menu, OpeningHour
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.


class MenuAdmin(SummernoteModelAdmin):
    summernote_fields = ("description", "name",)
    list_display = ("name","description", "price",)
    list_filter = ("name", "categories")
    search_fields = ("name", "categories")


admin.site.register(Menu, MenuAdmin)


class OpeningHourAdmin(admin.ModelAdmin):
    list_display = ( 'day_of_week', 'open_time', 'close_time')
    ordering = ('day_of_week',)


admin.site.register(OpeningHour, OpeningHourAdmin)
