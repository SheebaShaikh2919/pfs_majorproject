from django import forms
from main.models import Styles

class CreateStyledImageForm(forms.Form):
    content_image = forms.FileField(label='Upload Your Image')
    style = forms.ModelChoiceField(
        queryset=Styles.objects.all(),
        to_field_name='id',
        label='Choose a Style',
        empty_label='Select a Style',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['style'].queryset = Styles.objects.all()
