from rest_framework import serializers
from .models import *

class ServiceSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['pk', 'category']