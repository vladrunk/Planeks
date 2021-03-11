# workplace\views.py
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from .models import Schema, Column

import os
import json

from .tasks import generate_data_task, app


@login_required()
def index(request):
    user_schemas = Schema.objects.filter(user=request.user)
    context = {
        'schemas': user_schemas,
    }
    return render(request, 'workpalce/index.html', context)


@login_required()
def new_schema(request):
    return operate_schema(request=request, is_edit=False, schema_name='Default')


@login_required()
def edit_schema(request, schema_id):
    return operate_schema(request=request, is_edit=True, schema_id=schema_id)


def operate_schema(request, is_edit: bool, schema_id: int = None, schema_name: str = None):
    if is_edit:
        exist_schema, _schema = get_schema_from_db(pk=schema_id, user=request.user)
    else:
        exist_schema, _schema = get_schema_from_db(schema_name=schema_name)
    if not exist_schema:
        return _schema

    context = {
        'is_edit': is_edit,
        'schema': _schema,
        'columns': _schema.schema_columns.all(),
        'template_column': _schema.schema_columns.first(),
    }
    return render(request, 'workpalce/work_with_schema.html', context)


@login_required()
def submit_schema(request, schema_id=None):
    _schema, is_created = Schema.objects.update_or_create(
        user=request.user,
        pk=schema_id,
        defaults={
            'schema_name': request.POST.get('schema_name'),
            'column_separator': request.POST.get('column_separator'),
            'string_character': request.POST.get('string_character'),
        }
    )

    columns = sorted([row for row in zip(request.POST.getlist('column[][name]'),
                                         request.POST.getlist('column[][type]'),
                                         request.POST.getlist('column[][from]'),
                                         request.POST.getlist('column[][to]'),
                                         request.POST.getlist('column[][order]'))
                      ], key=lambda x: x[-1])

    if not is_created:
        _schema.schema_columns.all().delete()

    for column in columns:
        column_name, column_type, column_from, column_to, column_order = column
        Column.objects.create(
            schema=_schema,
            column_name=column_name,
            column_type=column_type,
            column_from=column_from,
            column_to=column_to,
            column_order=column_order,
        )

    return redirect(f'/schema/{_schema.pk}')


@login_required()
def delete_schema(request, schema_id):
    exist_schema, _schema = get_schema_from_db(pk=schema_id, user=request.user)
    if not exist_schema:
        return _schema

    if _schema.schema_datasets.all().count() > 0:
        dir_path = get_file_path(_schema.schema_datasets.all())
        for dataset in _schema.schema_datasets.all():
            dataset.file.delete()
        try:
            os.removedirs(dir_path)
        except FileNotFoundError:
            pass
    _schema.delete()
    return JsonResponse({'status': 'deleted',
                         'schema_id': schema_id,
                         }, status=200)


@login_required()
def schema(request, schema_id):
    exist_schema, _schema = get_schema_from_db(pk=schema_id, user=request.user)
    if not exist_schema:
        return _schema

    context = {
        'schema': _schema,
    }

    return render(request, 'workpalce/schema.html', context)


@login_required()
def generate_data(request, schema_id):
    try:
        nums_row = int(request.GET.get('nums_row'))
    except ValueError:
        nums_row = 1

    task = generate_data_task.delay(schema_id, request.user.pk, nums_row)

    return JsonResponse({'status': 'ok', 'task_id': task.id}, status=200)


@login_required()
def check_generate_data_status(request):
    if request.method == 'POST':
        tasks_from_site = json.loads(request.body)['task_id_list']
        tasks, urls = [], {}
        res = {'tasks': tasks, 'urls': urls}
        for task_id in tasks_from_site:
            task = app.AsyncResult(task_id)
            if task.successful():
                tasks.append(task.id)
                urls[task.id] = task.info['message']
        return JsonResponse(res, status=200)
    else:
        return JsonResponse({'message': f'Not allowed request method – {request.method}.'}, status=500)


def get_schema_from_db(*args, **kwargs):
    bad_response = JsonResponse({'status': 'error',
                                 'message': 'The scheme does not exist.',
                                 }, status=500)
    try:
        _schema = Schema.objects.get(*args, **kwargs)
    except ObjectDoesNotExist:
        return False, bad_response
    return True, _schema


def get_file_path(datasets):
    for dataset in datasets:
        try:
            return dataset.file.path.rsplit('\\', 1)[0]
        except ValueError:
            continue
    return ''
