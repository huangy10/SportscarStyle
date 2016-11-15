# coding=utf-8
from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

from .models import User, Sportscar, SportCarOwnership
from Club.models import ClubJoining
# Register your models here.


class MyUserChangeForm(UserChangeForm):

    class Meta(UserChangeForm.Meta):
        model = User

    def __init__(self, *args, **kwargs):
        super(MyUserChangeForm, self).__init__(*args, **kwargs)
        instance = kwargs.get("instance")
        if instance is not None:
            self.fields['avatar_car'].queryset = SportCarOwnership.objects.filter(
                user=instance
            )
            self.fields['avatar_club'].queryset = ClubJoining.objects.filter(user=instance)


class MyUserCreationForm(UserCreationForm):

    class Meta(UserChangeForm.Meta):
        model = User

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            User.objects.get(username=username)
        except ObjectDoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])


class AuthUserFilter(admin.SimpleListFilter):

    title = u'认证状态'
    parameter_name = u'auth_status'

    def lookups(self, request, model_admin):
        return (
            ('y', u'认证用户'),
            ('n', u'非认证用户'),
        )

    def queryset(self, request, queryset):
        if self.value() == "y":
            return queryset.filter(ownership__identified=True).distinct()
        elif self.value() == 'n':
            return queryset.filter(~Q(ownership__identified=True)).distinct()
        else:
            return queryset


@admin.register(User)
class MyUserAdmin(UserAdmin):

    form = MyUserChangeForm
    add_form = MyUserCreationForm

    fields = ("username", "password", "nick_name", "avatar", "avatar_club", "avatar_car",
              "gender", "birth_date", "star_sign", "district", "signature",
              "job", "corporation_identified", "fans_num", "follows_num",
              "status_num", "act_num", "value")
    readonly_fields = ('fans_num', 'follows_num', 'status_num', 'act_num', 'value')
    list_display = ('nick_name', 'username', "gender", "birth_date", "district", "value", )
    fieldsets = None
    search_fields = ("username", "nick_name")

    list_filter = (AuthUserFilter, )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

