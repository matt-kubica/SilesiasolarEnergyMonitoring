from rest_framework import generics, viewsets, views, status
# from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import LoginSerializer, RegisterSerializer, UserSerializer

from knox.models import AuthToken

from django.contrib.auth.models import User
from django.http import Http404


# TODO: superuser api

class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        print('LoginAPI -> post called')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


class UserAPI(views.APIView):

    def get(self, request, format=None):
        try:
            user = User.objects.get(id=request.user.id)
            serializer = UserSerializer(user, many=False)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)