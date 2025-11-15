from django.db import models


class SiteSetting(models.Model):
    site_name = models.CharField(max_length=100, verbose_name='نام سایت')
    site_url = models.CharField(max_length=200, verbose_name='دامنه سایت')
    address = models.CharField(max_length=200, verbose_name='آدرس')
    phone = models.CharField(max_length=20, null=True, blank=True, verbose_name='تلفن')
    fax = models.CharField(max_length=20, null=True, blank=True, verbose_name='فکس')
    email = models.CharField(max_length=200, null=True, blank=True, verbose_name='ایمیل')
    telegram = models.CharField(max_length=200, null=True, blank=True, verbose_name='تلگرام')
    facebook = models.CharField(max_length=200, null=True, blank=True, verbose_name='فیسبوک')
    twitter = models.CharField(max_length=200, null=True, blank=True, verbose_name='توییتر')
    instagram = models.CharField(max_length=200, null=True, blank=True, verbose_name='اینستاگرام')
    whatsapp = models.CharField(max_length=200, null=True, blank=True, verbose_name='واتساپ')
    copy_right = models.TextField(verbose_name='متن کپی رایت سایت')
    about_us_text = models.TextField(verbose_name='متن درباره ما سایت')
    site_logo = models.ImageField(upload_to='images/site-setting/', verbose_name='لوگو سایت')

    class Meta:
        verbose_name = 'تنظیمات سایت'
        verbose_name_plural = 'تنظیمات'

    def __str__(self):
        return self.site_name


class Slider(models.Model):
    name = models.CharField(max_length=50, verbose_name='نام')
    image = models.ImageField(upload_to='images/sliders', verbose_name='تصویر اسلایدر')
    is_active = models.BooleanField(default=True, verbose_name='فعال')

    class Meta:
        verbose_name = 'اسلایدر سایت'
        verbose_name_plural = 'اسلایدر های سایت'

    def __str__(self):
        return self.name


class HomeImageOrder(models.Model):
    name = models.CharField(max_length=50, verbose_name='نام')
    image = models.ImageField(upload_to='images/HomeImageReservation', verbose_name='عکس')
    is_active = models.BooleanField(default=True, verbose_name='فعال')

    class Meta:
        verbose_name = 'عکس صفحه خانه رستوران'
        verbose_name_plural = 'عکس های صفحه خانه رستوران'

    def __str__(self):
        return self.name


class SiteGallery(models.Model):
    name = models.CharField(max_length=50, verbose_name='نام')
    image = models.ImageField(upload_to='images/site-gallery', verbose_name='تصویر')
    is_active = models.BooleanField(default=True, verbose_name='فعال')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'تصویر گالری'
        verbose_name_plural = 'گالری تصاویر'
