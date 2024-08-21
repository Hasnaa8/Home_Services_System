from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.http.response import JsonResponse
from django.contrib import messages
from rest_framework.decorators import api_view, permission_classes
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated  # Add authentication if needed
from rest_framework import status, viewsets
# from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
# from drf_spectacular.types import OpenApiTypes
from users.permissions import *
from .models import Booking
from .serializers import BookingSerializer


class BookingView(APIView):
    permission_classes = [IsAuthenticated]  # Only authenticated users can create bookings
 
    def post(self, request, pk=None):
        if pk:
            serializer = BookingSerializer(data=request.data)
            if serializer.is_valid():
                provider = Profile.objects.get(pk=pk)
                if provider.is_craftsman:
                    # Access user from request (assuming user is authenticated)
                    serializer.save(customer=request.user.profile,
                                    customer_username=request.user.username,
                                    customer_fname=request.user.profile.fname,
                                    customer_lname=request.user.profile.lname,
                                    provider=provider, provider_username=provider.user.username, 
                                    home_address=request.user.profile.home_address,
                                    phone=request.user.profile.phone,
                                    service=provider.service, 
                                    service_category=provider.service.category)  # Set customer automatically
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EditBookingView(APIView):
    # permission_classes = [IsCutomerOrProvider]  # Only authenticated users can edit bookings

    def get_object(self, pk):
        try:
            return Booking.objects.get(pk=pk)
        except Booking.DoesNotExist:
            return None
    
    def get(self, request, pk=None):
        booking = self.get_object(pk)
        if booking:
            serializer = BookingSerializer(booking)
            return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    

    def put(self, request, pk):
        booking = self.get_object(pk)
        if not booking:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if booking.customer == request.user.profile:
            if booking.status == "completed":
                return Response({"error": "Appointment cannot be edited."}, status=status.HTTP_400_BAD_REQUEST)

            serializer = BookingSerializer(booking, data=request.data, partial=True)
            if serializer.is_valid():            
                serializer.validated_data['status'] = 'pending'

                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "Only customer can edit this appointment."}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        booking = self.get_object(pk)
        if booking.customer == request.user.profile or booking.provider == request.user.profile:

            if booking.status == "completed":
                return Response({"error": "Appointment cannot be deleted."}, status=status.HTTP_400_BAD_REQUEST)

            booking.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "Only Customer or Provider can delete this appointment."}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_orders_pending(request):
    if request.method == 'GET':
        bookings = Booking.objects.filter(customer=request.user.profile)
        pending = bookings.filter(status="pending")
        serializer = BookingSerializer(pending, many=True)

        return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_orders_confirmed(request):    
    if request.method == 'GET':
        bookings = Booking.objects.filter(customer=request.user.profile)
        confirmed = bookings.filter(status="confirmed")
        serializer = BookingSerializer(confirmed, many=True)

        return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_orders_completed(request):
    if request.method == 'GET':
        bookings = Booking.objects.filter(customer=request.user.profile)
        completed = bookings.filter(status="completed")
        serializer = BookingSerializer(completed, many=True)

        return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticatedAndIsCraftsman])
def my_schedule_pending(request):
    if request.method == 'GET':
        bookings = Booking.objects.filter(provider=request.user.profile)
        pending = bookings.filter(status="pending")
        serializer = BookingSerializer(pending, many=True)

        return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticatedAndIsCraftsman])
def my_schedule_confirmed(request):
    if request.method == 'GET':
        bookings = Booking.objects.filter(provider=request.user.profile)
        confirmed = bookings.filter(status="confirmed")
        serializer = BookingSerializer(confirmed, many=True)

        return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticatedAndIsCraftsman])
def my_schedule_completed(request):
    if request.method == 'GET':    
        bookings = Booking.objects.filter(provider=request.user.profile)
        completed = bookings.filter(status="completed")
        serializer = BookingSerializer(completed, many=True)

        return Response(serializer.data)

class BookingConfirmView(APIView):
    permission_classes = [IsAuthenticatedAndIsCraftsman] 
    def put(self, request, pk):
        booking = Booking.objects.get(pk=pk)
        if not booking:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if booking.provider != request.user.profile:
            return Response({"detail":"Only provider can confirm this appointment"},status=status.HTTP_400_BAD_REQUEST)


        if booking.status != "pending":
            return Response({"error": "Appointment cannot be confirmed in current status."}, status=status.HTTP_400_BAD_REQUEST)

        booking.status = "confirmed"
        booking.save()
        return Response({"message": "Appointment confirmed successfully."})

class BookingCompleteView(APIView):
    permission_classes = [IsAuthenticatedAndIsCraftsman]  
    def put(self, request, pk):
        booking = Booking.objects.get(pk=pk)
        if not booking:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if booking.provider != request.user.profile:
            return Response({"detail":"Only provider can confirm this appointment"}, status=status.HTTP_400_BAD_REQUEST)

        if booking.status != "confirmed":
            return Response({"error": "Appointment cannot be completed in current status."}, status=status.HTTP_400_BAD_REQUEST)

        booking.status = "completed"
        booking.save()
        return Response({"message": "Appointment completed successfully."})


