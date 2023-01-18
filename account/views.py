from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from account.serializers import (
    UserManagerSerializers,
    UserLoginSerializer,
    UserProfileSerializer,
    UserChangePasswordSerializer,
    SendPassEmailSerializer,
    UserPassResetSerializers
)
from django.contrib.auth import authenticate
from .renderers import UserRenderer
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = UserManagerSerializers(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response(
                {"token": token, "msg": "Registration sucess"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get("email")
            password = serializer.data.get("password")
            user = authenticate(email=email, password=password)
            print(password)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response(
                    {"token": token, "msg": "Login sucess"}, status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"errors": {"non_field_erors": ["Email or password is not valid"]}},
                    status=status.HTTP_404_NOT_FOUND,
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request, formate=None):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserChangePasswordView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request, formate=None):
        serializer = UserChangePasswordSerializer(
            data=request.data, context={"user": request.user}
        )
        if serializer.is_valid(raise_exception=True):
            return Response(
                {"msg": "Password Change Sucessfull"}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  

class SendPassEmailView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, formate=None):
        serializer =SendPassEmailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(
                {"msg": "Password Change Sucessfull"}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)      

class UserPassResetView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request,uid,token, formate=None):
        serializer = UserPassResetSerializers(data=request.data,context={'uid':uid,'token':token})
        if serializer.is_valid(raise_exception=True):
            return Response(
                {"msg": "Password Change Sucessfull"}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
