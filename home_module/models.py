from django.db import models


class Advantages(models.Model):
    summary_name = models.CharField(max_length=30, verbose_name='نام خلاصه')
    description = models.TextField(verbose_name='توضیحات')
    is_active = models.BooleanField(default=True, verbose_name='فعال')

    def __str__(self):
        return self.summary_name

    class Meta:
        verbose_name = 'مزیت'
        verbose_name_plural = 'مزایا'


class Introduction(models.Model):
    order = models.IntegerField(unique=True, verbose_name='ترتیب')
    description = models.TextField(verbose_name='توضیحات')
    is_active = models.BooleanField(default=True, verbose_name='فعال')

    def __str__(self):
        return f'پاراگراف {self.order}'

    class Meta:
        verbose_name = ' پاراگراف معرفی'
        verbose_name_plural = 'پاراگراف های معرفی'
