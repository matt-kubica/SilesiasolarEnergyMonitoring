from rest_framework import generics, viewsets, views, status
# from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

from .serializers import LoginSerializer, RegisterSerializer, UserSerializer

from knox.models import AuthToken

from django.contrib.auth.models import User
from django.http import Http404




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
            return Response({"error": "Permission denied"}, status=status.HTTP_401_UNAUTHORIZED)


class AdminUserAPI(views.APIView):
    permission_classes = [IsAdminUser, ]

    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    # TODO: post, put, delete

class AdminDetailUserAPI(views.APIView):
    permission_classes = [IsAdminUser, ]

    def get(self, request, pk, format=None):
        try:
            user = User.objects.get(id=pk)
            serializer = UserSerializer(user, many=False)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({"error": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)