from django import forms
from .models import Club


class ClubCreateForm(forms.ModelForm):

    class Meta:
        model = Club
        fields = ("name", "logo", "host", "description")
