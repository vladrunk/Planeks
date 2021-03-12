# workplace/models.py
from django.db import models

from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User


class Schema(models.Model):
    CHOISES_COLUMN_SEPARATOR = [
        ('comma', ',',),
        ('semicolon', ";"),
        ('colon', ':'),
    ]
    CHOISES_STRING_CHARACTER = [
        ('double_quote', '"',),
        ('apostrophe', "'"),
    ]
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
    )
    schema_name = models.CharField(
        default='',
        null=False,
        blank=False,
        max_length=255,
    )
    column_separator = models.CharField(
        default='comma',
        null=False,
        blank=False,
        max_length=9,
        choices=CHOISES_COLUMN_SEPARATOR,
    )
    string_character = models.CharField(
        default='double_quote',
        null=False,
        blank=False,
        max_length=12,
        choices=CHOISES_STRING_CHARACTER,
    )
    date_edit = models.DateTimeField(
        auto_now_add=True,
    )

    @staticmethod
    def get_char(chars, eq):
        return [char[1] for char in chars if char[0] == eq][0]

    def get_column_separator_char(self):
        return self.get_char(chars=self.CHOISES_COLUMN_SEPARATOR, eq=self.column_separator)

    def get_string_character_char(self):
        return self.get_char(chars=self.CHOISES_STRING_CHARACTER, eq=self.string_character)

    def __str__(self):
        return f'{self.schema_name}'


class Column(models.Model):
    CHOISES_COLUMN_TYPES = [
        ('full_name', 'Full name',),
        ('job', 'Job'),
        ('email', 'Email'),
        ('domain_name', 'Domain'),
        ('phone_number', 'Phone number'),
        ('company_name', 'Company'),
        ('text', 'Text'),
        ('integer', 'Integer'),
        ('address', 'Address'),
    ]
    schema = models.ForeignKey(
        to=Schema,
        related_name='schema_columns',
        default='',
        on_delete=models.CASCADE,
    )
    column_name = models.CharField(
        default='',
        null=False,
        blank=False,
        max_length=255,
    )
    column_type = models.CharField(
        default='',
        null=False,
        blank=False,
        max_length=15,
        choices=CHOISES_COLUMN_TYPES
    )
    column_from = models.PositiveIntegerField(
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ],
    )
    column_to = models.PositiveIntegerField(
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ],
    )
    column_order = models.IntegerField(
        default=0,
    )

    def __str__(self):
        return f'{self.schema.schema_name} {self.column_name}'


class DataSet(models.Model):
    schema = models.ForeignKey(
        to=Schema,
        related_name='schema_datasets',
        default='',
        on_delete=models.CASCADE,
    )
    date_create = models.DateTimeField(
        auto_now=True,
    )
    file_content = models.TextField(
        default=None,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f'{self.schema.schema_name} — {self.date_create}'
