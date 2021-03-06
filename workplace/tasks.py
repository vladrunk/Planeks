# workplace/tasks.py
import base64
from io import StringIO
import csv
import logging

import requests
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse

from Planeks.celery import app
from .models import Schema, DataSet


def __get_schema_from_db(*args, **kwargs):
    bad_response = JsonResponse({'status': 'error',
                                 'message': 'The scheme does not exist.',
                                 }, status=500)
    try:
        _schema = Schema.objects.get(*args, **kwargs)
    except ObjectDoesNotExist:
        return False, bad_response
    return True, _schema


def __fill_fields(columns):
    types = {
        'full_name': 'Full Name',
        'job': 'Job Title',
        'email': 'Email Address',
        'domain_name': 'Domain Name',
        'phone_number': 'Phone',
        'company_name': 'Company Name',
        'text': 'Paragraphs',
        'integer': 'Number',
        'address': 'Street Address'
    }

    fields = []

    for column in columns:
        fields.append({
            "name": column.column_name,
            "type": types[column.column_type],
            "min": column.column_from if column.column_type != 'text' else 1,
            "max": column.column_to if column.column_type != 'text' else 1,
            "percentBlank": 0,
            "decimals": 0
        })

    return fields


@app.task
def generate_data_task(schema_id, user_id, nums_row):
    exist_schema, _schema = __get_schema_from_db(pk=schema_id, user__pk=user_id)
    if not exist_schema:
        return _schema
    if not nums_row:
        logging.error("There is no number of lines in the parameters.")
        return {'status': 'error', 'message': 'There is no number of lines in the parameters.'}
    fields = __fill_fields(columns=_schema.schema_columns.all())
    url = 'https://www.mockaroo.com/api/generate.csv'
    payload = {'key': '2ef5da30', 'count': nums_row, }
    response = requests.post(url=url, params=payload, json=fields)
    if response.ok:
        content_b64 = __convertBytesToB64(content_bytes=response.content,
                                          delimiter=_schema.get_column_separator_char(),
                                          quote_char=_schema.get_string_character_char())
        dataset = DataSet.objects.create(schema=_schema, file_content=content_b64)
        if dataset:
            return {'status': 'ok', 'message': f'{dataset.pk}'}
        else:
            logging.error(f"Received incorrect CSV format")
            return {'status': 'error', 'message': 'Received incorrect CSV format.'}
    else:
        logging.error(f"Error while receiving data from the mockaroo")
        return {'status': 'error', 'message': 'Error while receiving data from the mockaroo.'}


def __convertBytesToB64(content_bytes: bytes, delimiter: str, quote_char: str):
    content = content_bytes.decode()
    with StringIO(content) as infile:
        reader = csv.DictReader(infile, delimiter=',')
        with StringIO() as outfile:
            writer = csv.DictWriter(
                outfile,
                delimiter=delimiter,
                quotechar=quote_char,
                lineterminator="\r",
                fieldnames=reader.fieldnames
            )
            writer.writeheader()
            writer.writerows(reader)
            res = base64.b64encode(outfile.getvalue().encode()).decode()
    return res
