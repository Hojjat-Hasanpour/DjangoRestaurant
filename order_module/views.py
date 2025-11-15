import time
import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import HttpRequest, JsonResponse, HttpResponse
from django.urls import reverse

from food_module.models import Food, FoodCapacity
from .models import Order, OrderDetail
from django.shortcuts import redirect, render
import requests
import json

# Create your views here.


MERCHANT = 'test'
ZP_API_REQUEST = "https://api.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = "https://api.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = "https://www.zarinpal.com/pg/StartPay/{authority}"
amount = 11000  # Rial / Required
description = "نهایی کردن خرید شما از سایت ما"  # Required
email = ''  # Optional
mobile = ''  # Optional
# Important: need to edit for realy server.
CallbackURL = 'http://127.0.0.1:8000/order/verify-payment/'


def add_food_to_order(request: HttpRequest):
    if not request.user.is_authenticated:
        return render(request, 'food_module/includes/toast_component.html', {
            'status': 'not_auth',
            'title': 'خطا در عملیات.',
            'message': 'لطفا برای افزودن غذا به لیست، ابتدا وارد شوید.',
        })

    try:
        food_id = int(request.GET.get('food_id'))
        count = int(request.GET.get('count'))
    except ValueError:
        return render(request, 'food_module/includes/toast_component.html', {
            'status': 'invalid_count_food_id',
            'title': 'خطا در عملیات.',
            'message': 'غذا یا تعداد وارد شده معتبر نمی باشد.',
        })

    if count < 1:
        return render(request, 'food_module/includes/toast_component.html', {
            'status': 'invalid_count',
            'title': 'خطا در عملیات.',
            'message': 'تعداد وارد شده معتبر نمی باشد.',
        })

    food = Food.objects.filter(id=food_id, is_active=True, is_delete=False).first()
    if food is not None:
        current_order, created = Order.objects.get_or_create(is_paid=False, user_id=request.user.id)
        current_order_detail = OrderDetail.objects.filter(order_id=current_order.id, food_id=food_id).first()

        try:
            today_food = FoodCapacity.objects.get(is_active=True, food=food, date=datetime.date.today())
        except ObjectDoesNotExist:
            return render(request, 'food_module/includes/toast_component.html', {
                'status': 'not_found',
                'title': 'خطا در عملیات.',
                'message': 'غذای مورد نظر برای امروز موجود نیست.',
            })

        today_sum = OrderDetail.objects.filter(order__is_paid=True, order__payment_date=datetime.date.today(),
                                               food=food).aggregate(Sum('count'))
        if today_sum['count__sum'] is None:
            today_sum['count__sum'] = 0

        if (today_food.capacity - today_sum['count__sum']) < count:
            return render(request, 'food_module/includes/toast_component.html', {
                'status': 'invalid_capacity',
                'title': 'خطا در عملیات.',
                'message': 'ظرفیت غذای امروز کافی نمی باشد. دوباره تلاش کنید.',
            })

        if current_order_detail is not None:
            current_order_detail.count = count
            current_order_detail.save()
        else:
            new_detail = OrderDetail(order_id=current_order.id, food_id=food_id, count=count)
            new_detail.save()

        return render(request, 'food_module/includes/toast_component.html', {
            'status': 'success',
            'title': 'عملیات موفقیت آمیز',
            'message': 'غذای مورد نظر با موفقیت به سبد خرید شما اضافه شد.',
        })

    else:
        return render(request, 'food_module/includes/toast_component.html', {
            'status': 'not_found',
            'title': 'خطا در عملیات.',
            'message': 'غذای مورد نظر یافت نشد',
        })


@login_required
def remove_food_order(request: HttpRequest):
    try:
        food_id = int(request.GET.get('food_id'))
    except ValueError:
        return render(request, 'food_module/includes/toast_component.html', {
            'status': 'food_id_not_an_number',
            'title': 'خطا در عملیات.',
            'message': 'آیدی غذای وارد شده صحیح نیست.'
        })

    current_order: Order = Order.objects.get(user_id=request.user.id, is_paid=False)
    deleted_count, deleted_dict = OrderDetail.objects.filter(order__is_paid=False, order__user_id=request.user.id,
                                                             food_id=food_id).delete()

    if deleted_count == 0:
        return render(request, 'food_module/includes/toast_component.html', {
            'status': 'detail_not_found',
            'title': 'خطا در عملیات.',
            'message': 'جزئیات یافت نشد.'
        })

    current_order_details: OrderDetail = OrderDetail.objects.filter(order__is_paid=False, order__id=current_order.id)

    context = {
        'current_order': current_order,
        'current_order_details': current_order_details,
        'status': 'success',
        'title': 'عملیات موفقیت آمیز',
        'message': 'غذا با موفقیت از سبد حذف شد.'

    }
    return render(request, 'account_module/includes/order_food_partial.html', context)


@login_required
def request_payment(request: HttpRequest):
    current_order, created = Order.objects.get_or_create(is_paid=False, user_id=request.user.id)
    total_price = current_order.calculate_total_price()
    if total_price == 0:
        return redirect(reverse('user_basket_page'))

    req_data = {
        "merchant_id": MERCHANT,
        "amount": total_price * 10,
        "callback_url": CallbackURL,
        "description": description,
        # "metadata": {"mobile": mobile, "email": email}
    }
    req_header = {"accept": "application/json", "content-type": "application/json'"}
    req = requests.post(url=ZP_API_REQUEST, data=json.dumps(req_data), headers=req_header)
    authority = req.json()['data']['authority']
    if len(req.json()['errors']) == 0:
        return redirect(ZP_API_STARTPAY.format(authority=authority))
    else:
        e_code = req.json()['errors']['code']
        e_message = req.json()['errors']['message']
        return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")


@login_required
def verify_payment(request: HttpRequest):
    current_order, created = Order.objects.get_or_create(is_paid=False, user_id=request.user.id)
    total_price = current_order.calculate_total_price()
    t_authority = request.GET['Authority']
    if request.GET.get('Status') == 'OK':
        req_header = {"accept": "application/json", "content-type": "application/json'"}
        req_data = {
            "merchant_id": MERCHANT,
            "amount": total_price * 10,
            "authority": t_authority
        }
        req = requests.post(url=ZP_API_VERIFY, data=json.dumps(req_data), headers=req_header)
        if len(req.json()['errors']) == 0:
            t_status = req.json()['data']['code']
            if t_status == 100:
                current_order.is_paid = True
                current_order.payment_date = time.time()
                current_order.save()
                ref_str = req.json()['data']['ref_id']
                return render(request, 'order_module/payment_result.html', {
                    'success': f'تراکنش شما با کد پیگیری {ref_str} با موفقیت انجام شد'
                })
            elif t_status == 101:
                return render(request, 'order_module/payment_result.html', {
                    'info': 'این تراکنش قبلا ثبت شده است'
                })
            else:
                # return HttpResponse('Transaction failed.\nStatus: ' + str(
                #     req.json()['data']['message']
                # ))
                return render(request, 'order_module/payment_result.html', {
                    'error': str(req.json()['data']['message'])
                })
        else:
            e_code = req.json()['errors']['code']
            e_message = req.json()['errors']['message']
            # return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")
            return render(request, 'order_module/payment_result.html', {
                'error': e_message
            })
    else:
        return render(request, 'order_module/payment_result.html', {
            'error': 'پرداخت با خطا مواجه شد / کاربر از پرداخت ممانعت کرد'
        })


@login_required
def success_payment(request):
    try:
        order_id = int(request.GET.get('order_id'))
        total_price = request.GET.get('total_price')
    except ValueError:
        return JsonResponse({
            'status': 'invalid_order_id_price',
            'message': 'شماره سفارش یا مقدار پرداختی معتبر نیست.',
        })
    try:
        current_order = Order.objects.get(id=order_id, user_id=request.user.id, is_paid=False)
    except ObjectDoesNotExist:
        return JsonResponse({
            'status': 'not_food_found',
            'message': 'سفارش مورد نظر وجود ندارد.',
        })

    if total_price != 0:
        current_order.is_paid = True
        current_order.payment_date = datetime.date.today()
        current_order.save()
        return JsonResponse({
            'status': 'success',
            'message': 'پرداخت شما موفقیت آمیز بود.',
        })
    else:
        return JsonResponse({
            'status': 'price_zero',
            'message': 'مقدار پرداختی صفر میباشد. سفارش کان لم یکن میشود.'
        })


@login_required
def cancel_payment(request):
    try:
        order_id = int(request.GET.get('order_id'))
        total_price = request.GET.get('total_price')
        if order_id < 0:
            raise ValueError('آیدی مورد نظر اشتباه است.')
    except ValueError:
        return JsonResponse({
            'status': 'invalid_order_id',
            'message': 'سبد خرید مورد نظر وجود ندارد.',
        })

    if total_price == 0:
        return JsonResponse({
            'status': 'price_zero',
            'message': 'مقدار پرداختی صفر میباشد. سفارش کان لم یکن میشود.',
        })

    current_order = Order.objects.get(user=request.user, is_paid=False, payment_date=None)
    current_order_details = OrderDetail.objects.filter(order=current_order).delete()
    current_order.delete()
    return JsonResponse({
        'status': 'failed',
        'message': 'کاربر از پرداخت مبلغ ممانعت کرد.',
    })
