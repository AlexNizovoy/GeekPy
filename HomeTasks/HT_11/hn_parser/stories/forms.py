from django import forms

from . import config as cfg


class GetNewRecordsForm(forms.Form):
    choices = [('all', 'All')]
    categories = [(i, i.capitalize()) for i in cfg.CATEGORIES]
    choices += categories
    category = forms.ChoiceField(choices=choices, label='Categories for get:')
    category.widget.attrs = {'class': 'form-control'}
