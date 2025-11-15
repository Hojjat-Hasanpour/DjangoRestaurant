from django.db import models
from jalali_date import date2jalali

from account_module.models import User
from food_module.models import Food


# Create your models here.

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    is_paid = models.BooleanField(verbose_name='پرداخت شده/پرداخت نشده')
    payment_date = models.DateField(null=True, blank=True, verbose_name='تاریخ پرداخت')

    def __str__(self):
        return f"{self.user} - {date2jalali(self.payment_date).strftime('%Y/%m/%d') if self.payment_date else '*'}"

    def calculate_total_price(self):
        total_amount = 0
        if self.is_paid:
            for order_detail in self.orderdetail_set.all():
                total_amount += order_detail.final_price * order_detail.count
        else:
            for order_detail in self.orderdetail_set.all():
                order_detail.final_price = order_detail.food.price
                order_detail.save()

            for order_detail in self.orderdetail_set.all():
                total_amount += order_detail.food.price * order_detail.count

        return total_amount

    class Meta:
        verbose_name = 'سبد خرید'
        verbose_name_plural = 'سبدهای خرید کاربران'


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='سبد خرید')
    food = models.ForeignKey(Food, on_delete=models.CASCADE, verbose_name='غذا')
    final_price = models.IntegerField(null=True, blank=True, verbose_name='قیمت نهایی تکی غذا')
    count = models.IntegerField(verbose_name='تعداد')

    def get_total_price(self):
        return self.count * self.food.price

    def __str__(self):
        return str(self.order)

    class Meta:
        verbose_name = 'جزییات سبد خرید'
        verbose_name_plural = 'لیست جزییات سبدهای خرید'
