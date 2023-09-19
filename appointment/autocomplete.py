from dal import autocomplete
from .models import Address

autocomplete.register(Address, search_fields=('cep',), attrs={
    'data-autocomplete-minimum-characters': 1,
})
