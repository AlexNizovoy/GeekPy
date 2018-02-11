from django.forms import ModelForm
from django import forms

from datetime import date

from todo.models import Project, Task


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'date_deadline']
        widgets = {
            'title': forms.TextInput(attrs={'size': 40}),
            'description': forms.TextInput(attrs={'size': 100}),
            'date_deadline': forms.SelectDateWidget
        }
    date_start = forms.DateField(widget=forms.DateInput(
        attrs={'value': date.today()}), disabled=True, required=False)

    def clean(self):
        cleaned_data = super(ProjectForm, self).clean()
        dt_start = date.today()
        dt_deadline = cleaned_data.get('date_deadline')
        if dt_start > dt_deadline:
            self.add_error('date_deadline', 'Deadline date in past time!')


class ProjectForm2(forms.Form):
    # test manual form
    title = forms.CharField(max_length=200)
    description = forms.CharField(max_length=300, empty_value='')
    date_start = forms.DateField(widget=forms.SelectDateWidget(
        empty_label=("Choose Year", "Choose Month", "Choose Day"),
    ), disabled=True)
    date_deadline = forms.DateField(widget=forms.SelectDateWidget(
        empty_label=("Choose Year", "Choose Month", "Choose Day"),
    ))


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'project']
        widgets = {
            'title': forms.TextInput(attrs={'size': 40}),
            'description': forms.TextInput(attrs={'size': 100}),
            'project': forms.TextInput(attrs={'readonly': '', 'size': 10})
        }
