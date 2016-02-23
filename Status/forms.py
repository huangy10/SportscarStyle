from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from django.contrib.gis.geos import Point

from .models import Status
from Sportscar.models import Sportscar
from Location.models import Location


class StatusCreationForm(forms.ModelForm):

    user_id = forms.IntegerField()
    car_id = forms.IntegerField(required=False)
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
        if car_id is None:
            return None
        try:
            car = Sportscar.objects.get(id=car_id)
        except ObjectDoesNotExist:
            raise forms.ValidationError(code='4000', message='Sport car not found.')
        return car

    class Meta:
        model = Status
        fields = ('image1', 'image2', 'image3', 'image4', 'image5', 'image6', 'image7', 'image8', 'image9', 'content')

    def save(self, commit=True):
        loc = Location.objects.create(
            location=Point(x=self.cleaned_data['lon'], y=self.cleaned_data['lat']),
            description=self.cleaned_data['location_description'],
        )
        status = Status.objects.create(
            user=self.cleaned_data['user_id'],
            car=self.cleaned_data['car_id'],
            image1=self.cleaned_data.get("image1", None),
            image2=self.cleaned_data.get("image2", None),
            image3=self.cleaned_data.get("image3", None),
            image4=self.cleaned_data.get("image4", None),
            image5=self.cleaned_data.get("image5", None),
            image6=self.cleaned_data.get("image6", None),
            image7=self.cleaned_data.get("image7", None),
            image8=self.cleaned_data.get("image8", None),
            image9=self.cleaned_data.get("image9", None),
            content=self.cleaned_data['content'],
            location=loc,
        )
        return status
