from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

from .models import AuthenticationCode, UserProfile, CorporationUserApplication
from .utils import star_sign_from_date


class RegistrationForm(UserCreationForm):

    auth_code = forms.CharField(max_length=6)

    def clean_password2(self):
        password = super(RegistrationForm, self).clean_password2()
        if len(password) < 4:
            raise forms.ValidationError('password too short', code='1003')
        return password

    def clean(self):
        super(RegistrationForm, self).clean()
        if 'username' not in self.cleaned_data:
            return
        auth_code = self.cleaned_data['auth_code']
        phone = self.cleaned_data['username']
        if not AuthenticationCode.objects.check_code(code=auth_code, phone=phone):
            self.add_error('auth_code', forms.ValidationError(
                'invalid code',
                code='1002'
            ))


class PasswordResetForm(forms.ModelForm):

    password1 = forms.CharField(max_length=100)
    password2 = forms.CharField(max_length=100)
    auth_code = forms.CharField(max_length=6)

    class Meta:
        model = get_user_model()
        fields = ('username', )

    def __init__(self, data=None, *args, **kwargs):
        super(PasswordResetForm, self).__init__(data, *args, **kwargs)
        self.user = None

    def clean_username(self):
        """ Check if the given username exists
        """
        phone = self.cleaned_data['username']
        try:
            self.user = get_user_model().objects.get(username=phone, is_active=True)
        except ObjectDoesNotExist:
            raise forms.ValidationError('invalid username', code='1000')
        return phone

    def clean_password2(self):
        password = self.cleaned_data['password2']
        if len(password) < 8:
            raise forms.ValidationError('password too short', code='1003')
        password1 = self.cleaned_data['password1']
        if not password == password1:
            raise forms.ValidationError('password mismatch.', code='1001')
        return password

    def clean(self):
        if 'username' not in self.cleaned_data:
            return
        auth_code = self.cleaned_data['auth_code']
        phone = self.cleaned_data['username']
        if not AuthenticationCode.objects.check_code(code=auth_code, phone=phone):
            self.add_error('auth_code', forms.ValidationError(
                'invalid code',
                code='1002'
            ))

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data['password1'])
        if commit:
            self.user.save()
        return self.user


class ProfileCreationForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ('nick_name', 'gender', 'birth_date', 'avatar')

    def __init__(self, profile, data=None, *args, **kwargs):
        super(ProfileCreationForm, self).__init__(data=data, *args, **kwargs)
        self.profile = profile

    def save(self, commit=True):
        profile = self.profile
        if 'nick_name' in self.cleaned_data:
            profile.nick_name = self.cleaned_data['nick_name']
        if 'gender' in self.cleaned_data:
            profile.gender = self.cleaned_data['gender']
        if 'birth_date' in self.cleaned_data:
            profile.birth_date = self.cleaned_data['birth_date']
            profile.star_sign = star_sign_from_date(profile.birth_date)
        if 'avatar' in self.cleaned_data:
            profile.avatar = self.cleaned_data["avatar"]
        if commit:
            profile.save()


class CorporationUserApplicationCreateForm(forms.ModelForm):

    class Meta:
        model = CorporationUserApplication
        fields = ("license_image", "id_card_image", "other_info_image", 'user')

