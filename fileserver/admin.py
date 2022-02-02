from django.contrib import admin

from .models import Url, File, IdBinding


@admin.register(File)
class RequestDemoAdmin(admin.ModelAdmin):
    list_display = ['id', 'file', 'filename']


@admin.register(Url)
class RequestDemoAdmin(admin.ModelAdmin):
    list_display = ['id', 'url']


@admin.register(IdBinding)
class RequestDemoAdmin(admin.ModelAdmin):
    list_display = [field.name for field in IdBinding._meta.get_fields()]
