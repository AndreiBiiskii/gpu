from django.contrib import admin

from device.models import Manual, Category


@admin.register(Manual, Category)
class ManualAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
