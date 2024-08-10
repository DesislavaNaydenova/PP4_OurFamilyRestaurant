from django.contrib import admin
from .models import Menu
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.


class MenuAdmin(SummernoteModelAdmin):
    summernote_fields = ("description", "name", "categories", "price",)
    list_display = ("name", "price", "categories")
    list_filter = ("name", "categories")
    search_fields = ("name", "categories")

admin.site.register(Menu, MenuAdmin)
