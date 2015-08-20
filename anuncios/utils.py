# -*- coding: utf-8 -*-
from __future__ import (unicode_literals, absolute_import, division,
                        print_function)

from django.conf import settings

def get_category_item(slug):
    """Return single category data object by slug with attached parents."""
    cat = settings.ANUNCIOS.CATEGORIES
    try:
        item = dict([x for x in cat if x['slug']==slug][0]) # copy this item
    except IndexError:
        return None
    if isinstance(item['parent'], (basestring, int)):
        item['parent'] = get_category_item(item['parent'])
    return item

def get_category_children(slug):
    """Return a list of category objects that are children if 'slug'."""
    return [x for x in settings.ANUNCIOS.CATEGORIES if x['parent']==slug]
