from product.forms import CurrencyAddForm, XlsUploadForm
from cart.forms import CartProductAddForm


def forms(request):
    return {'forms': {
        'currency_add': CurrencyAddForm(),
        'currency_upload': XlsUploadForm(),
        'add_to_cart': CartProductAddForm(),
    }}
