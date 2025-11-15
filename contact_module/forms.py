from django import forms
from django.core.exceptions import ValidationError

from contact_module.models import ContactUs


class ContactUsModelForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ['title', 'is_read_by_admin', 'message', 'parent']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'title',
            }),
            'is_read_by_admin': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'placeholder': 'false'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control h-250',
                'placeholder': 'متن پیام را دراین قسمت وارد نمایید.',
                # 'rows': 10,
            }),
            'parent': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'parent',
            })
        }
        labels = {
            'title': 'عنوان پیام',
            'is_read_by_admin': 'ارسال به صورت شخصی برای ادمین',
            'message': 'متن پیام',
            'parent': 'پاسخ به'
        }

        error_messages = {
            'title': {
                'required': 'عنوان پیام ضروری می باشد.'
            },
            'message': {
                'required': 'متن پیام ضروری می باشد.'
            }
        }
