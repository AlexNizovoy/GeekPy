from django import forms


class CartProductAddForm(forms.Form):
    product_id = forms.IntegerField(widget=forms.HiddenInput)


class CartInlineForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, max_value=20)
    product_id = forms.IntegerField()
    delete = forms.BooleanField(required=False)
