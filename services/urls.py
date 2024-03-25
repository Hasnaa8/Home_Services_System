from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import login, logout
urlpatterns = [
    path('', views.home, name='home'),
    # path('', views.about_us, name='about_us'),
    # path('', views.contact_us, name='contact_us'),
    # path('login/', login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    # path('', views.settings, name='settings'),
    # path('', views.profile, name='profile'),
    
    
    
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
