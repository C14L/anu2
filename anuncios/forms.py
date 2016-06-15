from django import forms
from django.core.urlresolvers import reverse_lazy

from anuncios.models import Post
from dtrcity.models import City


def _get_city_by_pk(pk):
    return City.objects.get(pk=pk).tr_crc


def _get_city_by_crc(crc):
    return City.get_by_crc(crc)


class AutocompleteField(forms.CharField):
    """
    Receives a City "crc" string from a input[type="text"] field and converts
    it into an instance of the model that the ForeignKey points to.
    """

    def __init__(self, fk_reverse_lookup, fk_forward_lookup,
                 autocomplete_url, autocomplete_query='q', *args, **kwargs):
        """
        Args:
            fk_reverse_lookup: A function to find an instance from input field.
            fk_forward_lookup: A function that returns the string for the input
                               field.
            autocomplete_url: The URL to query for autocomplete suggestions.
            autocomplete_query: The query parameter, default: q

        """
        # A method that returns an instance of the attached model.
        self.fk_reverse_lookup = fk_reverse_lookup
        self.fk_forward_lookup = fk_forward_lookup
        # The URL to load a JSON string with autocomplete values.
        self.autocomplete_url = autocomplete_url
        # The query variable for the request (default: 'q').
        self.autocomplete_query = autocomplete_query
        super().__init__(*args, **kwargs)

    def widget_attrs(self, widget):
        attrs = super().widget_attrs(widget)
        attrs['autocomplete-url'] = self.autocomplete_url
        attrs['autocomplete-query'] = self.autocomplete_query
        return attrs

    def to_python(self, value):
        model_instance = self.fk_reverse_lookup(value)
        return super().to_python(model_instance.pk)

    def prepare_value(self, value):
        print('############ prepare_value -> value: "{}"'.format(value))
        return self.fk_forward_lookup(value)

    def clean(self, value):
        return self.fk_reverse_lookup(value)


class PostForm(forms.ModelForm):
    city = AutocompleteField(_get_city_by_crc,
                             _get_city_by_pk,
                             reverse_lazy('city_autocomplete_crc'))

    class Meta:
        model = Post
        fields = ['title', 'text', 'city', 'categories', 'publish', 'expires',
                  'pic_1', 'pic_2', 'pic_3', 'pic_4', ]
        widgets = {
            'publish': forms.DateTimeInput(attrs={'type': 'date'}),
            'expires': forms.DateTimeInput(attrs={'type': 'date'}),
            'categories': forms.CheckboxSelectMultiple(),
        }
