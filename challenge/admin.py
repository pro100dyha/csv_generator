from django.contrib import admin
from .models import *


class SchemaFieldAdminInline(admin.TabularInline):
    model = SchemaField
    extra = 1


@admin.register(DataSchema)
class DataSchemaAdmin(admin.ModelAdmin):
    inlines = (SchemaFieldAdminInline, )
    list_display = ('name', 'date_modified')


@admin.register(DataSet)
class DataSetAdmin(admin.ModelAdmin):
    list_display = ('data_schema', 'csv_file')
