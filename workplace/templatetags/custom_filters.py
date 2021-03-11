from django import template

register = template.Library()


@register.filter(name='cap_choise_val')
def capitalized_choise_value(value):
    return f'{value[0].capitalize()} ({value[1]})'

