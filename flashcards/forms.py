from django import forms


class AddCardForm(forms.Form):
    word = forms.CharField(label='Word', max_length=255, required=True)
    definition = forms.CharField(label='Definition', max_length=255, required=True)
