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
    path('reserve/<int:facility_id>/', facility_views.reserve, name='reserve'),
    path('reservation_list/', facility_views.reservation_list, name='reservation_list'),
    path('cancellation/<int:reservation_id>', facility_views.cancellation_request, name='cancellation'),
    path('cancellation_request_list/', facility_views.cancellation_request_list, name='cancellation_request_list')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)