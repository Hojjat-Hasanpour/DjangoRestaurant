import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.contrib.auth import login, logout
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.utils.crypto import get_random_string
from django.utils.decorators import method_decorator

from order_module.models import Order, OrderDetail
from utils.email_service import send_email
from .models import User
from django.views import View
from django.views.generic import TemplateView

from account_module.forms import LoginForm, RegisterForm, ForgotPasswordForm, ForgetResetPasswordForm, \
    EditInformationForm, ResetPasswordForm


class RegisterView(View):
    def get(self, request):
        return render(request, 'account_module/register.html', {'register_form': RegisterForm()})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = register_form.cleaned_data.get('username')
            user_email = register_form.cleaned_data.get('email')
            user_password = register_form.cleaned_data.get('password')
            # user_confirm_password = register_form.cleaned_data.get('confirm_password')
            user_email_rep: bool = User.objects.filter(email__iexact=user_email).exists()
            user_name_rep: bool = User.objects.filter(email__iexact=user_name).exists()
            if user_email_rep or user_name_rep:
                if user_email_rep:
                    register_form.add_error('email', 'ایمیل وارد شده تکراری می باشد')
                if user_name_rep:
                    register_form.add_error('username', 'نام کاربری تکراری می باشد')
            else:
                new_user = User(
                    email=user_email,
                    email_active_code=get_random_string(72),
                    is_active=False,
                    username=user_name)
                new_user.set_password(user_password)
                new_user.save()
                messages.success(request, 'حساب شما با موفقیت ایجاد شد. جهت فعالسازی آن ایمیل خود را چک کنید. ')
                # send_email('فعالسازی حساب کاربری', new_user.email, {'user': new_user}, 'emails/activate_account.html')
                return render(request, 'account_module/login.html', {'login_form': LoginForm()})

        context = {
            'register_form': register_form
        }

        return render(request, 'account_module/register.html', context)


class LoginView(View):
    def get(self, request):
        context = {
            'login_form': LoginForm()
        }
        return render(request, 'account_module/login.html', context)

    def post(self, request: HttpRequest):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_email = login_form.cleaned_data.get('email')
            user_pass = login_form.cleaned_data.get('password')
            user: User = User.objects.filter(email__iexact=user_email).first()
            if user is not None:
                if not user.is_active:
                    login_form.add_error('email', 'حساب کاربری شما فعال نشده است')
                else:
                    is_password_correct = user.check_password(user_pass)
                    if is_password_correct:
                        login(request, user)
                        return redirect(reverse('dashboard_page'))
                    else:
                        login_form.add_error('email', 'نام کاربری یا کلمه عبور اشتباه است.')
            else:
                login_form.add_error('email', 'نام کاربری یا کلمه عبور اشتباه است.')

        context = {
            'login_form': login_form
        }

        return render(request, 'account_module/login.html', context)


class ForgetPasswordView(View):
    def get(self, request: HttpRequest):
        forget_pass_form = ForgotPasswordForm()
        context = {'forget_pass_form': forget_pass_form}
        return render(request, 'account_module/forget_password.html', context)

    def post(self, request: HttpRequest):
        forget_pass_form = ForgotPasswordForm(request.POST)
        if forget_pass_form.is_valid():
            user_email = forget_pass_form.cleaned_data.get('email')
            user: User = User.objects.filter(email__iexact=user_email).first()
            if user is not None:
                # user.email_active_code = get_random_string(72)
                send_email('بازیابی کلمه عبور', user.email, {'user': user}, 'emails/forgot_password.html')
                messages.success(request, 'کلمه عبور شما با موفقیت تغییر کرد.')
                return redirect(reverse('forget_reset_password_page'))
            forget_pass_form.add_error('email',
                                       'کاربری با آدرس ایمیل وارد شده یافت نشد. اگر حساب ندارید، ثبت نام کنید. ')

        context = {'forget_pass_form': forget_pass_form}
        return render(request, 'account_module/forget_password.html', context)


class ForgetResetPasswordView(View):
    def get(self, request: HttpRequest):
        return render(request, 'account_module/forget_reset_password.html',
                      {'reset_pass_form': ForgetResetPasswordForm()})

    def post(self, request: HttpRequest):
        reset_pass_form = ForgetResetPasswordForm(request.POST)
        # user: User = User.objects.filter(email_active_code__iexact=).first()
        if reset_pass_form.is_valid():
            user: User = User.objects.filter(email_active_code__iexact=reset_pass_form.cleaned_data.get(
                'email_active_code')).first()
            if user is None:
                reset_pass_form.add_error('email_active_code', 'کاربری با این کد فعالسازی پیدا نشد.')
                return render(request, 'account_module/forget_reset_password.html',
                              {'reset_pass_form': reset_pass_form})
            user_new_pass = reset_pass_form.cleaned_data.get('password')
            user.set_password(user_new_pass)
            user.email_active_code = get_random_string(72)
            user.is_active = True
            user.save()
            return redirect(reverse('login_page'))

        context = {
            'reset_pass_form': reset_pass_form,
        }

        return render(request, 'account_module/forget_reset_password.html', context)


@method_decorator(login_required, name='dispatch')
class ResetPasswordView(View):
    def get(self, request):
        context = {
            'reset_pass_form': ResetPasswordForm(),
        }
        return render(request, 'account_module/reset_password.html', context)

    def post(self, request):
        reset_pass_form = ResetPasswordForm(request.POST)
        if reset_pass_form.is_valid():
            user: User = User.objects.get(username=request.user.username)
            if not user.check_password(reset_pass_form.cleaned_data.get('password')):
                reset_pass_form.add_error('password', 'کلمه عبور اشتباه است.')
                return render(request, 'account_module/forget_reset_password.html',
                              {'reset_pass_form': reset_pass_form})

            user_new_pass = reset_pass_form.cleaned_data.get('new_password')
            user.set_password(user_new_pass)
            user.save()
            messages.success(request, 'کلمه عبور شما با موفقیت تغییر کرد.')
            return redirect(reverse('login_page'))

        context = {
            'reset_pass_form': reset_pass_form,
        }
        return render(request, 'account_module/forget_reset_password.html', context)


class ActivateAccountView(View):
    def get(self, request, email_active_code):
        user: User = User.objects.filter(email_active_code__iexact=email_active_code).first()
        if user is not None:
            if not user.is_active:
                user.is_active = True
                user.email_active_code = get_random_string(72)
                user.save()
                messages.success(request, 'حساب شما با موفقیت فعال شد.')
            else:
                messages.error(request, 'عملیات با خطا مواجه شد. کد فعالسازی قبلا وارد شده است.')
        else:
            messages.error(request, 'عملیات با خطا مواجه شد. کد فعالسازی اشتباه است.')
        return redirect(reverse('login_page'))


@method_decorator(login_required, name='dispatch')
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('home'))


@method_decorator(login_required, name='dispatch')
class DashboardTemplateView(TemplateView):
    template_name = 'account_module/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardTemplateView, self).get_context_data()

        user_orders: Order = Order.objects.filter(user_id=self.request.user, is_paid=True).prefetch_related(
            'orderdetail_set')
        context['user_orders'] = user_orders

        return context


@method_decorator(login_required, name='dispatch')
class DemoPayment(View):
    def get(self, request):
        try:
            current_order = Order.objects.get(user_id=request.user.id, is_paid=False)
            current_order_detail = OrderDetail.objects.filter(order__exact=current_order)
            total_price = current_order.calculate_total_price()
        except ObjectDoesNotExist:
            current_order = None
            current_order_detail = None
            total_price = 0
        context = {
            'current_order': current_order,
            'current_order_detail': current_order_detail,
            'total_price': total_price,
            'date': datetime.date.today()
        }

        return render(request, 'account_module/demo_payment.html', context)


@method_decorator(login_required, name='dispatch')
class EditInformationView(View):  # UpdateView => obj.save()
    def get(self, request):
        form = EditInformationForm(instance=self.request.user)
        context = {
            'form': form
        }
        return render(request, 'account_module/edit_information.html', context)

    def post(self, request):
        edit_form = EditInformationForm(request.POST, instance=request.user)

        if edit_form.is_valid():
            user_exist_email = User.objects.get(email=edit_form.cleaned_data.get('email'))  # .first()  # todo
            if not user_exist_email or user_exist_email == request.user:
                user = request.user
                user.username = edit_form.cleaned_data.get('username')
                user.first_name = edit_form.cleaned_data.get('first_name')
                user.last_name = edit_form.cleaned_data.get('last_name')
                user.email = edit_form.cleaned_data.get('email')
                # Todo send email
                user.is_active = False
                user.save()
                # obj.update()
                messages.success(
                    self.request,
                    'اطلاعات با موفقیت ویرایش شد. جهت فعالسازی حساب کاربری لطفا به ایمیل خود مراجعه فرمایید.')
                return redirect(reverse('login_page'))
            else:
                edit_form.add_error('email', 'کاربری با این ایمیل وجود دارد.')
        else:
            messages.error(self.request, 'خطا در عملیات')
        return render(request, 'account_module/edit_information.html', {'form': edit_form})


@login_required
def order_food_component(request: HttpRequest):
    current_order, created = Order.objects.get_or_create(user_id=request.user.id, is_paid=False)
    current_order_details: OrderDetail = OrderDetail.objects.filter(order__is_paid=False, order_id=current_order.id)

    context = {
        'current_order': current_order,
        'current_order_details': current_order_details,
    }
    return render(request, 'account_module/includes/order_food_partial.html', context)
