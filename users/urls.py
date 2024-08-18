from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import login, logout
from rest_framework.routers import DefaultRouter
from .views import *
app_name = "users"

# router = DefaultRouter()
# router.register(r'favourites', FavouriteView, basename='favourites')

urlpatterns = [

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
