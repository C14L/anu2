from django import forms
from django.core.urlresolvers import reverse_lazy

from anuncios.models import Post
from basicautocomplete.forms import AutocompleteField
from dtrcity.models import City


def _get_city_crc_by_pk(pk):
    """Return the string to be displayed in the <input> field."""
    if isinstance(pk, str):
        return pk
    return City.objects.get(pk=pk).tr_crc


def _get_city_by_crc(crc):
    """Return the database object found by the string from the <input> field."""
    return City.get_by_crc(crc)


def normalize_email(email):
    try:
        email_name, domain_part = email.strip().rsplit('@', 1)
    except ValueError:
        pass
    else:
        email = '@'.join([email_name, domain_part.lower()])
    return email


class PostForm(forms.ModelForm):
    city = AutocompleteField(_get_city_by_crc,
                             _get_city_crc_by_pk,
                             reverse_lazy('city_autocomplete_crc'))

    class Meta:
        model = Post
        fields = ['title', 'text', 'city', 'email', 'categories', 'publish',
                  'expires', 'pic_1', 'pic_2', 'pic_3', 'pic_4', ]
        widgets = {
            'publish': forms.DateTimeInput(attrs={'type': 'date'}),
            'expires': forms.DateTimeInput(attrs={'type': 'date'}),
            'categories': forms.CheckboxSelectMultiple(),
        }

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data['email'] = normalize_email(cleaned_data['email'])
        return cleaned_data
