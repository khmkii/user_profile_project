from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.core import validators
from django.forms import (
        CharField, DateInput, EmailField, Form, FileInput,
        HiddenInput, ModelForm, TextInput, ValidationError,
        PasswordInput, FileField
    )

from collections import namedtuple
from bs4 import BeautifulSoup

from . import models
from accounts.validators import password_checker, check_empty


TempUserObject = namedtuple('TempUserObject', ['username', 'first_name', 'last_name'])


class UserAuthenticationForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise ValidationError(
                message="Account inactive, cant log you in",
                code='Inactive',
            )


class SignUpForm(Form):
    username = CharField(required=True)
    first_name = CharField(required=True)
    last_name = CharField(required=True)
    email = EmailField(
        required=True,
        validators=[validators.EmailValidator()]
    )
    confirm_email = EmailField(
        required=True,
        label="Confirm email"
    )
    tar_pit_trap = CharField(
        required=False,
        widget=HiddenInput,
        label="leave this blank",
        validators=[check_empty]
    )
    password = CharField(
        required=True,
        widget=PasswordInput,
        label='Create password',
    )

    confirm_password = CharField(
        required=True,
        widget=PasswordInput,
        label='Confirm password'
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError(
                "The username {} is in use already".format(username),
                code='TakenUsername'
            )
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError(
                message="The email {} is in use already".format(email),
                code="TakenEmail",
            )
        return email

    def clean_password(self):
        password = self.cleaned_data['password']
        temp_user_obj = TempUserObject(
            username=self.cleaned_data['username'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name']
        )
        p_check = password_checker(password, userObj=temp_user_obj)
        if p_check is not None:
            error = '\n'.join(p_check)
            raise ValidationError(
                message=error,
                code='BadPassword'
            )
        return password

    def clean(self):
        data = super().clean()
        email1 = data.get('email')
        email2 = data.get('confirm_email')
        if email1 != email2:
            raise ValidationError(
                message='Emails do not match!',
                code="DoesNotMatchEmail",
            )
        p1 = data.get('password')
        p2 = data.get('confirm_password')
        if p1 != p2:
            raise ValidationError(
                message='Passwords do not match!',
                code='DoesNotMatchPassword'
            )


class EditProfileForm(ModelForm):
    avatar = FileField(
        label="Upload Your Profile Picture Here",
        widget=FileInput,
        required=False
    )

    class Meta:
        model = models.UserProfile
        fields = (
            'date_of_birth',
            'biography',
        )
        widgets = {
            'date_of_birth': DateInput(attrs={
                'class': 'datepicker',
            }),
            'biography': TextInput(attrs={
                'class': 'textarea',
            }),
        }
        labels = {
            'date_of_birth': 'Date of birth'
        }

    def clean_biography(self):
        bio = BeautifulSoup(
            self.cleaned_data['biography'],
            'html5lib'
        ).get_text(strip=True)
        if len(bio) < 10:
            raise ValidationError(
                "Your Biography should be more than 10 characters"
            )
        return bio


class ChangePasswordForm(Form):
    current_password = CharField(
        required=True,
        widget=PasswordInput,
    )
    new_password = CharField(
        required=True,
        widget=PasswordInput,
    )
    confirm_new_password = CharField(
        required=True,
        widget=PasswordInput,
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    def clean_old_password(self):
        current_password = self.cleaned_data.get('current_password')
        if not check_password(current_password, self.user.password):
            raise ValidationError(
                "You current password is incorrect"
            )
        return current_password

    def clean_new_password(self):
        new_password = self.cleaned_data['new_password']
        val_fails = password_checker(new_password, userObj=self.user, oldPword=self.user.password)
        if val_fails:
            error = '\n'.join(val_fails)
            raise ValidationError(
                message=error,
                code='BadPassword'
            )
        return new_password

    def clean(self):
        data = super().clean()
        new_password1 = data.get('new_password', None).strip()
        new_password2 = data.get('confirm_new_password', None).strip()
        if new_password1 != new_password2:
            raise ValidationError(
                message='Passwords do not match!',
                code='DoesNotMatchPassword'
            )
