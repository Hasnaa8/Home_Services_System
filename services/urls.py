from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('', views.about_us, name='about_us'),
    path('', views.contact_us, name='contact_us'),
    path('', views.login, name='login'),
    path('', views.signup, name='signup'),
    path('', views.logout, name='logout'),
    path('', views.settings, name='settings'),
    path('', views.profile, name='profile'),
    
    
    
]
