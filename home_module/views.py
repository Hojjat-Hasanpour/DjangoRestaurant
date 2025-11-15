from django.shortcuts import render
from django.views.generic import TemplateView, ListView

from home_module.models import Advantages, Introduction
from food_module.models import FoodCategory
from services_module.models import Services
# todo from service_module.models import Services
from site_module.models import SiteSetting, Slider, HomeImageOrder, SiteGallery


# from utils.convertor import group_list


class HomeView(TemplateView):
    template_name = 'home_module/index.html'

    def get_context_data(self, **kwargs):
        setting: SiteSetting = SiteSetting.objects.filter(site_name__iexact='رستوران سجاد').first()
        slider: Slider = Slider.objects.filter(is_active=True)
        image_order: HomeImageOrder = HomeImageOrder.objects.filter(is_active=True).first()
        food_category: FoodCategory = FoodCategory.objects.filter(is_active=True)
        services = Services.objects.filter(is_active=True)[:6]
        context = super().get_context_data(**kwargs)
        context['site_setting'] = setting
        context['slider'] = slider
        context['image_order'] = image_order
        context['food_categories'] = food_category
        context['services'] = services
        return context


def site_header_component(request):
    setting: SiteSetting = SiteSetting.objects.filter(site_name__iexact='رستوران سجاد').first()
    context = {
        'site_setting': setting
    }
    return render(request, 'shared/site_header_component.html', context)


def site_footer_component(request):
    setting: SiteSetting = SiteSetting.objects.filter(site_name__iexact='رستوران سجاد').first()
    services: Services = Services.objects.filter(is_active=True)[:4]
    context = {
        'site_setting': setting,
        'services': services
    }
    return render(request, 'shared/site_footer_component.html', context)


class AdvantagesView(TemplateView):
    template_name = 'home_module/advantage.html'

    def get_context_data(self, **kwargs):
        advantages: Advantages = Advantages.objects.filter(is_active=True)
        context = super().get_context_data(**kwargs)
        context['advantages'] = advantages
        return context


class IntroductionView(TemplateView):
    template_name = 'home_module/introduction.html'

    def get_context_data(self, **kwargs):
        intros: Introduction = Introduction.objects.filter(is_active=True).order_by('order')
        context = super().get_context_data(**kwargs)
        context['introductions'] = intros
        return context
