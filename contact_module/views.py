from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.contrib import messages
from django.views.generic import CreateView

from contact_module.forms import ContactUsModelForm
from contact_module.models import ContactUs

from site_module.models import HomeImageOrder


# class ContactUsView(View):
#     comments: ContactUs = ContactUs.objects.filter(is_active=True, parent=None,
#                                                    is_read_by_admin=False).prefetch_related('contactus_set')
#     context = {
#         'comments': comments,
#         'count': ContactUs.objects.filter(is_active=True, is_read_by_admin=False).count(),
#         'action': '',
#         # 'message': ''
#     }
#
#     def get(self, request):
#         form = ContactUsModelForm()
#         self.context['form'] = form
#         # self.context['message'] = ''
#         # self.context['action'] = ''
#         # print(self.context['comments'])
#         return render(request, 'contact_module/contact_us.html', self.context)
#
#     def post(self, request):
#         form = ContactUsModelForm(request.POST)
#
#         if form.is_valid():
#             obj = form.save(commit=False)
#             obj.user = self.request.user
#             self.request.POST.get('')
#             obj.save()
#             self.context['action'] = 'True'
#             messages.success(self.request, 'پیام شما با موفقیت ارسال شد و در دست بررسی است.')
#             # return render(request, 'contact_module/contact_us.html', self.context)
#
#         else:
#             messages.error(self.request, 'پیام شما با خطا مواجه شد.')
#         #     self.context['action'] = 'False'
#         #     self.context['message'] = 'پیام شما با خطا مواجه شده است.'
#         # return render(request, 'contact_module/contact_us.html', self.context)
#
#         return redirect(reverse('contact_us_page'))


class ContactUsCreateView(CreateView):
    form_class = ContactUsModelForm
    model = ContactUs
    template_name = 'contact_module/contact_us.html'
    success_url = '/contact-us/'

    def get_context_data(self, **kwargs):
        context = super(ContactUsCreateView, self).get_context_data()
        # comments:
        context['comments']: ContactUs = ContactUs.objects.filter(is_active=True, parent=None).prefetch_related(
            'contactus_set')
        # context['comments']: ContactUs = ContactUs.objects.filter(is_active=True, parent=None).select_related('')
        context['current_user'] = self.request.user
        context['image_form'] = HomeImageOrder.objects.filter(is_active=True).first()
        return context

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        # messages.add_message(request=self.request, message='پیام شما با موفقیت ارسال شد و در دست بررسی است.')
        messages.success(self.request, 'پیام شما با موفقیت ارسال شد و در دست بررسی است.')
        return super(ContactUsCreateView, self).form_valid(form)

    def form_invalid(self, form):
        # messages.add_message(request=self.request, message='پیام شما با خطا مواجه شد.')
        messages.error(self.request, 'پیام شما با خطا مواجه شد.')
        return super(ContactUsCreateView, self).form_invalid(form)
