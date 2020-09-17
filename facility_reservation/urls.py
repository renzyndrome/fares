from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from users import views as user_views
from facility import views as facility_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',user_views.home, name='home'),
    path('admin/', admin.site.urls),
    path('register/', user_views.register, name='register'),
    path('profile/', user_views.profile, name='profile'),
    path('view_user/<int:user_id>/', user_views.view_user, name='view_user'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('password-reset/',
                    auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'),
                    name='password_reset'),
    path('password-reset/done/',
                    auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
                    name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
                    auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
                    name='password_reset_confirm'),
    path('password-reset-complete/',
                    auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
                    name='password_reset_complete'),
    path('user_list/', user_views.user_list, name='user_list'),
    path('facility/',facility_views.facility, name='facility_list'),
    path('facility/<int:facility_id>/', facility_views.facility_detail, name='facility_detail'),
    path('vehicle/',facility_views.vehicle_list, name='vehicle_list'),
    path('vehicle/<int:vehicle_id>/', facility_views.vehicle_detail, name='vehicle_detail'),
    path('reserve/facility/<int:facility_id>/', facility_views.reserve_facility, name='reserve_facility'),
    path('reserve/vehicle/<int:vehicle_id>/', facility_views.reserve_vehicle, name='reserve_vehicle'),
    path('pay-with-funds/', facility_views.pay_with_funds, name='pay-with-funds'),
    path('vehicle-pay-with-funds/', facility_views.vehicle_pay_with_funds, name='vehicle-pay-with-funds'),
    path('facility-create-payment-intent/', facility_views.facility_create_payment, name='facility-create-payment-intent'),
    path('vehicle-create-payment-intent/', facility_views.vehicle_create_payment, name='vehicle-create-payment-intent'),
    path('facility-payment-complete/', facility_views.facility_payment_complete, name='facility-payment-complete'),
    path('vehicle-payment-complete/', facility_views.vehicle_payment_complete, name='vehicle-payment-complete'),
    path('reservation_list/', facility_views.user_reservation_list, name='user_reservation_list'),
    path('admin_reservation_list/', facility_views.admin_reservation_list, name='admin_reservation_list'),
    path('reserve/insufficient-balance/', facility_views.insufficient_balance, name='insufficient_balance'),
    path('reserve/already_reserved/', facility_views.already_reserved, name='already_reserved'),
    path('cancellation/<int:reservation_id>/', facility_views.cancellation_request, name='cancellation'),
    path('approve_cancellation/<int:reservation_id>/', facility_views.approve_cancellation, name='approve_cancellation'),
    path('income/', facility_views.weekly_income, name='income'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)