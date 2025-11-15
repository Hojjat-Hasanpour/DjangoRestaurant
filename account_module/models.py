from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


# Create your models here.
class User(AbstractUser):
    email_active_code = models.CharField(max_length=100, verbose_name='کد فعالسازی ایمیل')

    def __str__(self):
        if self.first_name != '' and self.last_name != '':
            return self.get_full_name()

        return self.username

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        if self.email is None or self.email == '':
            raise ValidationError({'email': 'وارد کردن ایمیل الزامی است.'})
