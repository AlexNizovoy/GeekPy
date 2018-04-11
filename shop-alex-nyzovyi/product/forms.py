from django import forms

from product.models import Currency, Product
from product.forms_snippet import SubmitButtonField


class CurrencyAddForm(forms.ModelForm):
    class Meta:
        model = Currency
        fields = '__all__'


class XlsUploadForm(forms.Form):
    xls_file = forms.FileField()
    submit = SubmitButtonField(label="", initial="Upload file")


class ProductAddForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
