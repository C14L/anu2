import re
from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def personal_data_filter(value):
    patterns = [
        re.compile(r'\w+@(?:aol|gmail|hotmail|mail|tagoror\.net)', flags=re.IGNORECASE),
        re.compile(r'\d{5,}'),
    ]

    for p in patterns:
        value = p.sub('---', value)
    return value
