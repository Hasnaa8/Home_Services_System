from django.shortcuts import render, redirect, get_object_or_404 # type: ignore
from django.contrib.auth.forms import UserCreationForm # type: ignore
from django.http import HttpResponse, HttpResponseRedirect # type: ignore
from django.contrib import messages # type: ignore
from .forms import *
from django.contrib.auth import authenticate, login, logout # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from django.contrib.auth.forms import PasswordChangeForm # type: ignore
from django.contrib.auth import update_session_auth_hash # type: ignore
from .models import *
from bookings.models import *
from rest_framework.decorators import api_view 
from rest_framework.response import Response 
from rest_framework.views import APIView 
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import generics, status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate # type: ignore
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from .permissions import *
from .serializers import *


# register view - create user - create token
class RegisterView(APIView):
    # permission_classes = [AllowAny]  # Allow anyone to register

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = authenticate(username=username, password=password)
        login(request, user)

        token, created = Token.objects.get_or_create(user=user)
        profile = CustomerProfileSerializer(user.profile)

        return Response({'profile':profile.data,'token': token.key}, status=status.HTTP_201_CREATED)

# login view - authenticate user - create token
class LoginView(APIView):
    # permission_classes = [AllowAny]  # Allow anyone to register

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            if user.profile.is_craftsman:
                profile = ProviderProfileSerializer(user.profile, context={'request': request})
            else:
                profile = CustomerProfileSerializer(user.profile)
            return Response({'profile':profile.data,'token': token.key}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

# logout view - delete token
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        Token.objects.get(key=request.user.auth_token).delete()
        return Response(status=status.HTTP_200_OK)
    
# profile view - 
class ProfileView(APIView):
    permission_classes = [OwnProfileOrReadOnly]  # Require authentication for profile update
    # authentication_classes = [TokenAuthentication]
    def get(self, request, pk=None):
        if pk:
            profile = get_object_or_404(Profile, pk=pk)
        else:
            profile = request.user.profile
        if profile.is_craftsman:
            serializer = ProviderProfileSerializer(profile, context={'request': request})
        else :
            serializer = CustomerProfileSerializer(profile)
        return Response(serializer.data)
    
# edit personal profile info 
class PersonalInfoView(APIView):
    #user has that accounts
    permission_classes = [OwnProfileOrReadOnly]  # Require authentication for profile update
    # authentication_classes = [TokenAuthentication]

    def get(self, request):
        profile = request.user.profile
        serializer = PersonalInfoSerializer(profile)
        return Response(serializer.data)
    
    def put(self, request):
        profile = request.user.profile
        serializer = PersonalInfoSerializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

#if craftsman => edit work info
class WorkInfoView(APIView):
    #user has that account and craftsman
    permission_classes = [IsAuthenticatedAndIsCraftsman, OwnProfileOrReadOnly]  # Require authentication for profile update
    # authentication_classes = [TokenAuthentication]

    def get(self, request):
        profile = request.user.profile
        serializer = WorkInfoSerializer(profile)
        return Response(serializer.data)
    
    def put(self, request):
        profile = request.user.profile
        serializer = WorkInfoSerializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

# change pass - check pass - set pass
class ChangePasswordView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']
            confirm_new_password = serializer.validated_data['confirm_new_password']

            user = request.user
            if not user.check_password(old_password):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)

            if new_password != confirm_new_password:
                return Response({"password & confirm": ["didn't match."]}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(new_password)
            user.save()
            return Response({"detail": "Password has been changed."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# change email - check pass - email = newemail
class ChangeEmailView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = ChangeEmailSerializer(data=request.data)
        if serializer.is_valid():
            password = serializer.validated_data['password']
            new_email = serializer.validated_data['new_email']

            user = request.user
            if not user.check_password(password):
                return Response({"password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)

            user.email = new_email
            user.save()
            return Response({"detail": "Email has been changed."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   

# delete user
class DeleteUserView(generics.GenericAPIView):
    serializer_class = DeleteUserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    # to get user's account
    def get_object(self):
        return self.request.user
    
    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class FavView(APIView):
    def get(self, request):
        user = request.user
        favs = Fav.objects.filter(profile=user.profile)
        profiles = Profile.objects.filter(fav_profile__in=favs)
        serialized_profiles = FavSerializer(profiles, context={"request":request}, many=True)
        return Response(serialized_profiles.data)

@api_view(['POST'])
def edit_fav_list(request, pk):
    user = request.user
    fav_profile = Profile.objects.get(pk=pk)
    if user == fav_profile :
        Response({'detail': 'Cannot add/delete yourself to/from favourites'}, status=status.HTTP_400_BAD_REQUEST)
    
    if fav_profile.is_craftsman:
        fav, created = Fav.objects.get_or_create(profile=user.profile, fav_profile=fav_profile)
        if created:
            return Response({'detail': 'User added to favourites'}, status=status.HTTP_200_OK)
        else:
            fav.delete()
            return Response({'detail': 'User removed from favourites'}, status=status.HTTP_204_NO_CONTENT)
    else :
        return Response({'detail': 'Cannot add normal user to favourite'}, status=status.HTTP_400_BAD_REQUEST)
