from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from account_module.models import User
import datetime


class FoodCategory(models.Model):
    name = models.CharField(max_length=300, db_index=True, verbose_name='عنوان')
    slug = models.SlugField(max_length=150, null=False, db_index=True, allow_unicode=True, editable=False,
                            verbose_name='عنوان در url')
    image = models.ImageField(upload_to='images/foodCategories', verbose_name='تصویر دسته بندی غذا')
    is_active = models.BooleanField(verbose_name='فعال / غیرفعال')
    is_delete = models.BooleanField(verbose_name='حذف شده / نشده')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'

    def create_unique_slug(self, food_category_id, food_category_slug):
        find_category = FoodCategory.objects.filter(slug__iexact=food_category_slug)
        if find_category.exists():
            food_category_slug = f'{food_category_slug}-{food_category_id}'
            self.create_unique_slug(food_category_id, food_category_slug)

        return food_category_slug

    def get_absolute_url(self):
        return reverse('food_category_page', args=[self.slug])

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, allow_unicode=True)
        self.slug = self.create_unique_slug(self.id, self.slug)
        super().save(*args, **kwargs)


class Food(models.Model):
    name = models.CharField(max_length=300, verbose_name='نام غذا')
    category = models.ForeignKey(FoodCategory, on_delete=models.CASCADE, verbose_name='دسته بندی')
    image = models.ImageField(upload_to='images/foods', null=True, blank=True, verbose_name='تصویر غذا')
    price = models.IntegerField(verbose_name='قیمت')
    short_description = models.CharField(max_length=255, null=True, verbose_name='توضیحات کوتاه')
    description = models.TextField(verbose_name='توضیحات اصلی')
    slug = models.SlugField(default="", null=False, db_index=True, blank=True, max_length=200, unique=True,
                            verbose_name='عنوان در url')
    is_active = models.BooleanField(default=True, verbose_name='فعال / غیرفعال')
    is_delete = models.BooleanField(verbose_name='حذف شده / نشده')

    def get_absolute_url(self):
        return reverse('food_detail_page', args=[self.slug])

    def create_unique_slug(self, food_id, food_slug):
        find_food = Food.objects.filter(slug__iexact=food_slug)
        if find_food.exists():
            food_slug = f'{food_slug}-{food_id}'
            self.create_unique_slug(food_id, food_slug)

        return food_slug

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, allow_unicode=True)
        self.slug = self.create_unique_slug(self.id, self.slug)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.price})"

    class Meta:
        verbose_name = 'غذا'
        verbose_name_plural = 'غذاها'


class FoodCapacity(models.Model):
    food = models.ForeignKey(Food, on_delete=models.CASCADE, verbose_name='غذا')
    date = models.DateField(verbose_name='تاریخ روز')
    is_active = models.BooleanField(default=True, verbose_name='فعال / غیرفعال')
    capacity = models.IntegerField(verbose_name='ظرفیت غذای روزانه',
                                   validators=[MaxValueValidator(100), MinValueValidator(1)])

    def __str__(self):
        return f'{self.food} - {self.capacity}'

    def clean(self):
        if self.capacity <= 0 or self.capacity > 100:
            raise ValidationError({'capacity': 'مقدار وارد شده صحیح نمی باشد.'})
        if self.date < datetime.date.today():
            raise ValidationError({'date': 'شما نمیتوانید برای روزهای گذشته ظرفیت وارد کنید.'})

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
        # if self.capacity <= 0 or self.capacity > 100:
        #     raise ValidationError({'capacity': 'مقدار وارد شده صحیح نمی باشد.'})

    class Meta:
        verbose_name = 'ظرفیت غذا'
        verbose_name_plural = 'ظرفیت غذاها'
