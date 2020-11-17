from django.forms import ModelForm
from django import forms
from .models import Note


class DateInput(forms.DateInput):
    input_type = 'date'


class DateForm(forms.Form):
    my_date_field = forms.DateField(widget=DateInput(attrs={'class': 'form-control'}))


class NoteForm(ModelForm):
    date_added = forms.DateField(widget=DateInput(attrs={'class': 'form-control'}))
    meal = forms.ChoiceField(choices=Note.MEAL_TYPE, widget=forms.Select(attrs={'class': 'form-control'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))

    class Meta:
        model = Note
        fields = ['date_added', 'meal', 'description']
