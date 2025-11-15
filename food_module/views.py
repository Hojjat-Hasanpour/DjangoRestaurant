import datetime

from django.db.models import Prefetch
from django.shortcuts import render
from django.views.generic import TemplateView, DetailView

from food_module.models import Food, FoodCategory, FoodCapacity


class FoodTemplateView(TemplateView):
    template_name = 'food_module/food_list.html'

    def get_context_data(self, **kwargs):
        context = super(FoodTemplateView, self).get_context_data()
        categories = FoodCategory.objects.filter(
            is_active=True, food__foodcapacity__capacity__gt=0,
            food__foodcapacity__date=datetime.date.today()).distinct().prefetch_related('food_set')

        context['categories'] = categories
        return context


def toast_component(request):
    context = {
        'status': '',
        'title': '',
        'message': ''
    }
    return render(request, 'food_module/includes/toast_component.html', context)


class FoodDetailView(DetailView):
    template_name = 'food_module/food_detail.html'
    model = Food

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context["now"] = timezone.now()
        return context
