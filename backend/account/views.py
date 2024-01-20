from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from account.serializers import *
from account.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated 

from account.models import EmailConfirmationToken

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token)
    }

# Create your views here.
class UserRegistrationView(APIView):
    renderer_classes = (UserRenderer,)
    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token= get_tokens_for_user(user)
            return Response({'token':token, 'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response({'msg': 'Registration failed'}, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    renderer_classes = (UserRenderer,)
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                token= get_tokens_for_user(user)
                return Response({'token':token, 'message': 'Login successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'errors':{'non_field_errors':['Email or password is not valid']}}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    renderer_classes = (UserRenderer,)  # Assuming UserRenderer is defined
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        email = request.user.email
        is_email_verified = request.user.is_email_verified
        serializer = UserProfileSerializer(request.user)  # Pass user instance as data
        return Response({'email': email, 'is_email_verified': is_email_verified, 'data': serializer.data}, status=status.HTTP_200_OK)
    
# class UserEmailVerificationView(APIView):
#     permission_classes = (IsAuthenticated,)
#     def post(self, request, format=None):
#        user = request.user
#        token = EmailConfirmationToken.objects.create(user=user)
#        send_confirmation_email(user.email, token.token, user.id)
#        return Response({'message': 'Email verification link has been sent to your email'}, status=status.HTTP_200_OK)


class UserChangePasswordView(APIView):
    renderer_classes = (UserRenderer,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        serializer = UserChangePasswordSerializer(data=request.data, context={'user': request.user})
        if serializer.is_valid(raise_exception=True):
            return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class SendPasswordResetEmailView(APIView):
    renderer_classes = (UserRenderer,)
    def post(self, request, format=None):
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({'message': 'Password reset email has been sent.'}, status=status.HTTP_200_OK)
        
class UserPasswordResetView(APIView):
    renderer_classes = (UserRenderer,)
    def post(self, request, uid, token, format=None):
        serializer = UserPasswordResetSerializer(data=request.data, context={'uid': uid, 'token': token})
        if serializer.is_valid(raise_exception=True):
            return Response({'message': 'Password reset successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

