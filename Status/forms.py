from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from django.contrib.gis.geos import Point

from .models import Status
from Sportscar.models import Sportscar
from Location.models import Location


class StatusCreationForm(forms.ModelForm):

    user_id = forms.IntegerField()
    car_id = forms.IntegerField()
    lat = forms.FloatField()
    lon = forms.FloatField()
    location_description = forms.CharField(max_length=255)

    def clean_user_id(self):
        user_id = self.cleaned_data['user_id']
        try:
            user = get_user_model().objects.get(id=user_id)
        except ObjectDoesNotExist:
            raise forms.ValidationError(code='4001', message='User not found.')
        return user

    def clean_car_id(self):
        car_id = self.cleaned_data['car_id']
        try:
            car = Sportscar.objects.get(id=car_id)
        except ObjectDoesNotExist:
            raise forms.ValidationError(code='4000', message='Sport car not found.')
        return car

    class Meta:
        model = Status
        fields = ('image', 'content')

    def save(self, commit=True):
        loc = Location.objects.create(
            location=Point(x=self.cleaned_data['lon'], y=self.cleaned_data['lat']),
            description=self.cleaned_data['location_description'],
            user=self.cleaned_data['user_id']
        )
        status = Status.objects.create(
            user=self.cleaned_data['user_id'],
            car=self.cleaned_data['car_id'],
            image=self.cleaned_data['image'],
            content=self.cleaned_data['content'],
            location=loc,
        )
        return status
