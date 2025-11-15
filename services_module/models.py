from django.db import models

from django.urls import reverse
from django.utils.text import slugify


class Services(models.Model):
    title = models.CharField(max_length=100, verbose_name='عنوان خدمت')
    short_description = models.CharField(max_length=250, verbose_name='توضیحات کوتاه')
    description = models.TextField(verbose_name='توضیحات اصلی')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    image = models.ImageField(upload_to='images/services', verbose_name='تصویر')
    logo = models.ImageField(upload_to='images/services', verbose_name='لوگو')
    slug = models.SlugField(max_length=100, db_index=True, allow_unicode=True, unique=True, null=False, blank=True,
                            editable=False, verbose_name='عنوان در url')

    class Meta:
        verbose_name = 'خدمت'
        verbose_name_plural = 'خدمات'

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse('service_detail_page', args=[self.slug])

    def create_unique_slug(self, service_id, service_slug):
        find_service = Services.objects.filter(slug__iexact=service_slug)
        if find_service.exists():
            service_slug = f'{service_slug}-{service_id}'
            self.create_unique_slug(service_id, service_slug)

        return service_slug

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        self.slug = self.create_unique_slug(self.id, self.slug)
        super().save(*args, **kwargs)
