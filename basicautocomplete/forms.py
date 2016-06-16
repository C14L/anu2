from django import forms


class AutocompleteField(forms.CharField):

    class Media:
        css = {'screen': ('basicautocomplete.css', ), }
        js = ('basicautocomplete.js', )

    def __init__(self, fk_reverse_lookup, fk_forward_lookup,
                 autocomplete_url, autocomplete_query='q', *args, **kwargs):
        """
        Args:
            fk_reverse_lookup: A function that takes as an argument the string
                               returned by the form and converts it into an
                               instance of a model.
            fk_forward_lookup: A function that takes a PK as an argument and
                               returns the string that is displayed in the HTML
                               input field.
            autocomplete_url: The URL to query for autocomplete suggestions. The
                              API returns a JSON list of completed strings.
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
        return self.fk_forward_lookup(value)

    def clean(self, value):
        return self.fk_reverse_lookup(value)
