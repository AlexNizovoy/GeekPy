from django import forms


class CartProductAddForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, max_value=20, initial=1)

    next = forms.CharField(max_length=50, widget=forms.HiddenInput)
    product_id = forms.IntegerField(widget=forms.HiddenInput)


class CartInlineForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, max_value=20)
    product_id = forms.IntegerField()
