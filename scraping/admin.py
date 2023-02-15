from django.contrib import admin
from .models import Link, City


# Register your models here.
admin.site.register(City)


@admin.register(Link)
class ScrapingAdmin(admin.ModelAdmin):
    list_display = ['link', 'room', 'region', 'address', 'price', 'city']
    list_editable = ['region', 'city', 'price']
    list_per_page = 30
