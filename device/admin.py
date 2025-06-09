from django.contrib import admin

from device.models import Manual, Category, Unit, Equipment


@admin.register(Manual, Category)
class ManualAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Unit)
class ManualAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Equipment)
class ManualAdmin(admin.ModelAdmin):
    list_display = ['serial_number', 'model']
    list_filter = ('name', 'si__unit')
