from django import forms


class AddCardForm(forms.Form):
    word = forms.CharField(label='Word', max_length=255, required=True)
    definition = forms.CharField(label='Definition', max_length=255, required=True)

    def __init__(self, *args, **kwargs):
        super(AddCardForm, self).__init__(*args, **kwargs)

        self.fields['word'].widget.attrs['class'] = 'form-control default-field'
        self.fields['definition'].widget.attrs['class'] = 'form-control default-field'
