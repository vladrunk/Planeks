# workplace/admin.py
from django.contrib import admin

from .models import *


@admin.register(Schema)
class SchemaAdmin(admin.ModelAdmin):
    fields = [
        'user', 'schema_name',
        'column_separator', 'string_character',
    ]
    list_display = [
        'id', 'user', 'schema_name',
        'column_separator', 'string_character', 'date_edit',
    ]


@admin.register(Column)
class ColumnAdmin(admin.ModelAdmin):
    fields = [
        'schema', 'column_name',
        'column_type', 'column_from',
        'column_to', 'column_order',
    ]
    list_display = ['id', 'schema', 'column_name', 'column_type', 'column_order', ]


@admin.register(DataSet)
class DataSetAdmin(admin.ModelAdmin):
    list_display = ['id', 'schema', 'date_create', 'file', ]

    def get_field_queryset(self, db, db_field, request):
        return db_field.remote_field.model.objects.filter(user=request.user)
