from django import forms
from django.contrib.auth import get_user_model

from .models import Club


class ClubCreateForm(forms.ModelForm):

    class Meta:
        model = Club
        fields = ("name", "logo", "host", "description")
