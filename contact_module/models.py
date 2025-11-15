from django.db import models

from account_module.models import User


class ContactUs(models.Model):
    title = models.CharField(max_length=150, verbose_name='عنوان')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    message = models.TextField(verbose_name='متن ارتباط با ما')
    create_date = models.DateField(verbose_name='تاریخ ارسال', auto_now_add=True)
    is_read_by_admin = models.BooleanField(default=False, verbose_name='ارسال شخصی برای ادمین')
    is_active = models.BooleanField(default=False, verbose_name='فعال (نمایش در سایت)')
    parent = models.ForeignKey('ContactUs', on_delete=models.CASCADE, verbose_name='والد نظر', null=True, blank=True)

    class Meta:
        verbose_name = 'ارتباط با ما'
        verbose_name_plural = 'لیست ارتباط با ما'

    def __str__(self):
        return f'{self.user.username}'
