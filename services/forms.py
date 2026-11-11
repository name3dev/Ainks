
from django import forms
from .models import ShortLink


class ShortLinkForm(forms.ModelForm):

    class Meta:
        model = ShortLink
        fields = ['title', 'original_url']

        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Например: Мой YouTube',
                'class': 'form-input'
            }),

            'original_url': forms.URLInput(attrs={
                'placeholder': 'https://youtube.com',
                'class': 'form-input'
            }),
        }
