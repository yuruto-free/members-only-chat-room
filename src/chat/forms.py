from django import forms
from django.utils.translation import gettext_lazy
from . import models

User = models.User

class SearchForm(forms.Form):
    keywords = forms.CharField(
        label=gettext_lazy('keywords (split space)'),
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': gettext_lazy('Enter the room name.'),
            'class': 'form-control',
        }),
    )

    def get_keywords(self):
        init_keywords = ''
        keywords = init_keywords

        if self.is_valid():
            keywords = self.cleaned_data.get('keywords', init_keywords)

        return keywords

class RoomForm(forms.ModelForm):
    class Meta:
        model = models.Room
        fields = ('name', 'description', 'participants')
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': gettext_lazy('Enter the room name.'),
                'class': 'form-control',
            }),
            'description': forms.Textarea(attrs={
                'rows': 5,
                'cols': 10,
                'style': 'resize: none',
                'placeholder': gettext_lazy('Enter the description.'),
                'class': 'form-control',
            }),
            'participants': forms.SelectMultiple(attrs={
                'class': 'form-control',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['participants'].queryset = User.objects.filter(is_staff=False)