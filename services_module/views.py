from django.views.generic import ListView, DetailView
from services_module.models import Services


class ServicesListView(ListView):
    model = Services
    template_name = 'service_module/'  # Not Set, no link in pages to return this template, Expand for later
    context_object_name = 'services'
    paginate_by = 9

    def get_queryset(self):
        query = super(ServicesListView, self).get_queryset()
        query.filter(is_active=True)
        return query


class ServicesDetailView(DetailView):
    model = Services
    template_name = 'service_module/services_detail.html'
    context_object_name = 'service'

    def get_queryset(self):
        query = super(ServicesDetailView, self).get_queryset()
        query.filter(is_active=True)
        return query
