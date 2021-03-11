# workpalce/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='workpalce'),
    path('schema/<int:schema_id>', schema, name='schema'),
    path('generate_data/<int:schema_id>', generate_data, name='generate_data'),
    path('check_generate_data', check_generate_data_status, name='check_generate_data_status'),
    path('new_schema', new_schema, name='new_schema'),
    path('edit_schema/<int:schema_id>', edit_schema, name='edit_schema'),
    path('submit_schema', submit_schema, name='submit_new_schema'),
    path('submit_schema/<int:schema_id>', submit_schema, name='submit_edit_schema'),
    path('delete_schema/<int:schema_id>', delete_schema, name='delete_schema'),
]
