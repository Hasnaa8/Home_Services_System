from rest_framework import serializers
from .models import *


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__' 

class EditBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['pk', 'date', 'time']

class UpdateStatusBooking(serializers.ModelSerializer):
    pass
