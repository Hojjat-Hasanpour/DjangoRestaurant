import datetime

from django import forms
from django.core import validators
from django.core.exceptions import ValidationError
from jalali_date.fields import JalaliDateField
from jalali_date.widgets import AdminJalaliDateWidget

from account_module.models import User


class RegisterForm(forms.Form):
    # username = forms.CharField(widget=forms.CharField(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    username = forms.CharField(
        label='نام کاربری',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
        validators=[
            validators.MaxLengthValidator(100)
        ]
    )

    email = forms.EmailField(
        label='ایمیل',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'name@example.com'}),
        validators=[
            validators.MaxLengthValidator(100),
            validators.EmailValidator
        ]
    )

    password = forms.CharField(
        label='کلمه عبور',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        validators=[
            validators.MaxLengthValidator(100)
        ]
    )
    confirm_password = forms.CharField(
        label='تکرار کلمه عبور',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password == confirm_password:
            return confirm_password
        raise ValidationError('کلمه عبور و تکرار کلمه عبور مغایرت دارند')


class LoginForm(forms.Form):
    email = forms.EmailField(
        label='ایمیل',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'name@example.com'}),
        validators=[
            validators.MaxLengthValidator(100),
            validators.EmailValidator
        ]
    )
    password = forms.CharField(
        label='کلمه عبور',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        validators=[
            validators.MaxLengthValidator(100)
        ]
    )


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(
        label='ایمیل',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'test@test.com'}),
        validators=[
            validators.MaxLengthValidator(100),
            validators.EmailValidator
        ]
    )


class ForgetResetPasswordForm(forms.Form):
    email_active_code = forms.CharField(
        label='کد فعالسازی ارسال شده',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        validators=[
            validators.MaxLengthValidator(72),
        ]
    )

    password = forms.CharField(
        label='کلمه عبور',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )

    confirm_password = forms.CharField(
        label='تکرار کلمه عبور',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password == confirm_password:
            return confirm_password
        raise ValidationError('کلمه عبور و تکرار کلمه عبور مغایرت دارند')


class ResetPasswordForm(forms.Form):
    password = forms.CharField(
        label='کلمه عبور قبلی',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )

    new_password = forms.CharField(
        label='کلمه عبور جدید',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )

    confirm_password = forms.CharField(
        label='تکرار کلمه عبور جدید',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )

    # def clean_new_password(self):
    #     password = self.cleaned_data.get('password')
    #     new_password = self.cleaned_data.get('new_password')
    #
    #     if not password == new_password:
    #         return new_password
    #     raise ValidationError('خطا!.کلمه عبور قبلی و جدید یکسان هستند.')

    def clean_confirm_password(self):
        new_password = self.cleaned_data.get('new_password')
        confirm_password = self.cleaned_data.get('confirm_password')

        # if new_password is None:
        #     return confirm_password

        if new_password == confirm_password:
            return confirm_password
        raise ValidationError('کلمه عبور و تکرار کلمه عبور مغایرت دارند')


class EditInformationForm(forms.ModelForm):
    # first_name = forms.CharField(
    #     label='نام',
    #     widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام'}),
    #     required=False
    # ),
    # last_name = forms.CharField(
    #     label='نام خانوادگی',
    #     widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام خانوادگی'}),
    #     required=False
    # ),
    # username = forms.CharField(
    #     label='نام',
    #     widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام کاربری'}),
    # ),
    # email = forms.EmailField(
    #     label='نام',
    #     widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ایمیل'}),
    # ),
    #
    # def __init__(self, *args, **kwargs):
    #     self.request = kwargs.pop('request')
    #     super(EditInformationForm, self).__init__(*args, **kwargs)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'firstname'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'firstname'
            }),
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'firstname'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'firstname'
            }),
        }
        labels = {
            'first_name': 'نام',
            'last_name': 'نام خانوادگی',
            'username': 'نام کاربری',
            'email': 'ایمیل'
        }

        error_messages = {
            'username': {
                'required': 'وارد کردن نام کاربری ضروری می باشد.'
            },
            'email': {
                'required': 'وارد کردن ایمیل الزامی می باشد.'
            }
        }

    # # def __init__(self, *args, **kwargs):
    # #     user = kwargs['user']
    # #     super(EditInformationModelForm, self).__init__(*args, **kwargs)
    # #     self.fields['first_name'] = user.first_name
    # #     self.fields['last_name'] = user.last_name
    # #     self.fields['email'] = user.email
    # #     self.fields['username'] = user.username
