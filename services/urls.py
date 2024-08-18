from django.urls import path,include

from rest_framework.routers import DefaultRouter
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import login, logout
from .views import *

router = DefaultRouter()
router.register(r'profiles', ProvidersViewSet)

urlpatterns = [
    path('', views.home, name='home'),
    path('<int:pk>/', views.providers_list, name='providers_list'),
    path('', include(router.urls)),

    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
