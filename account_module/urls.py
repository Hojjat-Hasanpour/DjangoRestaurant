from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register_page'),
    path('login/', views.LoginView.as_view(), name='login_page'),
    path('logout/', views.LogoutView.as_view(), name='logout_page'),
    path('forget-pass/', views.ForgetPasswordView.as_view(), name='forget_password_page'),
    path('forget-reset-pass/', views.ForgetResetPasswordView.as_view(), name='forget_reset_password_page'),
    path('reset-pass/', views.ResetPasswordView.as_view(), name='reset_password_page'),
    path('dashboard/', views.DashboardTemplateView.as_view(), name='dashboard_page'),
    path('payment/', views.DemoPayment.as_view(), name='demo_payment_page'),
    path('edit-information/', views.EditInformationView.as_view(), name='edit_information_page'),
    path('activate-account/<email_active_code>', views.ActivateAccountView.as_view(), name='activate_account_page'),
]
