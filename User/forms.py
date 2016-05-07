import datetime
import os

from django import forms
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from .models import User, CorporationAuthenticationRequest
from .models import AuthenticationCode
from Profile.utils import star_sign_from_date


class RegistrationForm(forms.ModelForm):

    auth_code = forms.CharField(max_length=6)

    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('User exists', code='1003')
        return username

    def clean_password(self):
        password = self.cleaned_data["password"]
        if len(password) < 4 or len(password) > 50:
            raise forms.ValidationError('Password length error', code='1003')
        return password

    def clean(self):
        super(RegistrationForm, self).clean()
        if 'username' not in self.cleaned_data or 'password' not in self.cleaned_data:
            # Error occurs in property validator
            return
        auth_code = self.cleaned_data['auth_code']
        phone = self.cleaned_data['username']
        if not AuthenticationCode.objects.check_code(code=auth_code, phone=phone):
            self.add_error('auth_code', forms.ValidationError(
                'invalid code',
                code='1002'
            ))

    def save(self, commit=True):
        user = User.objects.create(
            username=self.cleaned_data['username'],
            birth_date=datetime.date(year=1970, month=1, day=1),
            avatar=os.path.join('defaults', settings.DEFAULT_AVATAR_NAME),
            gender='m'
        )
        user.set_password(self.cleaned_data['password'])
        user.save()
        AuthenticationCode.objects.deactivate(
            code=self.cleaned_data['auth_code'],
            phone=self.cleaned_data['username']
        )
        return user

    class Meta:
        model = User
        fields = ("username", "password", "auth_code")


class PasswordResetForm(forms.ModelForm):
    password = forms.CharField(max_length=100)
    auth_code = forms.CharField(max_length=6)

    class Meta:
        model = User
        fields = ('username', )

    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)
        self.user = None

    def clean_username(self):
        phone = self.cleaned_data['username']
        try:
            self.user = User.objects.get(username=phone)
        except ObjectDoesNotExist:
            raise forms.ValidationError('invalid username', code='1000')
        return phone

    def clean_password(self):
        password = self.cleaned_data["password"]
        if len(password) < 4 or len(password) > 50:
            raise forms.ValidationError('Password length error', code='1003')
        return password

    def clean(self):
        if 'username' not in self.cleaned_data or 'password' not in self.cleaned_data:
            return
        auth_code = self.cleaned_data['auth_code']
        phone = self.cleaned_data['username']
        if not AuthenticationCode.objects.check_code(code=auth_code, phone=phone):
            self.add_error('auth_code', forms.ValidationError(
                'invalid code',
                code='1002'
            ))

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data['password'])
        AuthenticationCode.objects.deactivate(
            code=self.cleaned_data['auth_code'],
            phone=self.cleaned_data['username']
        )
        if commit:
            self.user.save()
        return self.user


class CorporationUserApplicationCreateForm(forms.ModelForm):

    class Meta:
        model = CorporationAuthenticationRequest
        fields = ("license_image", "id_card_image", 'other_info_image', 'user')


