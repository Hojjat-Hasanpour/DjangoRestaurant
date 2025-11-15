from django.urls import path
from . import views

urlpatterns = [
    path('add-food-to-order', views.add_food_to_order, name='add_food_to_order'),
    path('remove-from-order', views.remove_food_order, name='remove_food_order'),
    path('request-payment/', views.request_payment, name='request_payment'),  # ZarrinPal
    path('verify-payment/', views.verify_payment, name='verify_payment'),  # ZarrinPal
    path('success-payment/', views.success_payment, name='success_payment_page'),
    path('cancel-payment/', views.cancel_payment, name='cancel_payment_page'),
]
