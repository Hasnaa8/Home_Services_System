"""
URL configuration for HSPro project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from users import views as user_views
from bookings import views as booking_views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken.views import obtain_auth_token
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    
    path('register/', user_views.RegisterView.as_view(), name='register'),
    
    path('login/', user_views.LoginView.as_view(), name='login'),
    
    path('logout/', user_views.LogoutView.as_view(), name='logout'),
    
    path('profile/', user_views.ProfileView.as_view(), name='profile'),
    
    path('profiles/<int:pk>/', user_views.ProfileView.as_view(), name='profile'),
    
    path('edit-profile/', user_views.PersonalInfoView.as_view(), name='edit_profile'),
    
    path('edit-work-info/', user_views.WorkInfoView.as_view(), name='edit_work_info'),
    
    path('password-change/', user_views.ChangePasswordView.as_view(), name='password_change'),
    
    path('email-change/', user_views.ChangeEmailView.as_view(), name='email_change'),
    
    path('delete-account/', user_views.DeleteUserView.as_view(), name='delete_account'),
    
    path('booking_user/<int:pk>/', booking_views.BookingView.as_view(), name='booking_user' ),
    
    path('edit_booking/<int:pk>' ,booking_views.EditBookingView.as_view(), name='edit_booking'),
    
    path('complete_appointment/<int:pk>' ,booking_views.BookingCompleteView.as_view(), name='complete_appointment'),
    
    path('confirm_appointment/<int:pk>' ,booking_views.BookingConfirmView.as_view(), name='confirm_appointment'),
    
    path('my_orders_pending/' ,booking_views.my_orders_pending, name='my_orders_pending'),
    
    path('my_orders_confirmed/' ,booking_views.my_orders_confirmed, name='my_orders_confirmed'),
    
    path('my_orders_completed/' ,booking_views.my_orders_completed, name='my_orders_completed'),
    
    path('my_schedule_pending/' ,booking_views.my_schedule_pending, name='my_schedule_pending'),
    
    path('my_schedule_confirmed/' ,booking_views.my_schedule_confirmed, name='my_schedule_confirmed'),
    
    path('my_schedule_completed/' ,booking_views.my_schedule_completed, name='my_schedule_completed'),
    
    path('my_fav_list/' ,user_views.FavView.as_view(), name='my_fav_list'),

    path('edit_fav_list/<int:pk>/' ,user_views.edit_fav_list, name='edit_fav_list'),
    
    path('users', include('users.urls')),
    
    path('', include('services.urls')),
    
    path('api-auth/', include('rest_framework.urls')),
    path('api-token-auth/', obtain_auth_token),
    
    
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
