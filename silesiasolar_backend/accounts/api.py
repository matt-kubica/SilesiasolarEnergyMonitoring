from rest_framework import generics, views, status
from rest_framework.response import Response

from .serializers import LoginSerializer, RegisterSerializer, UserSerializer
from .models import User

from knox.models import AuthToken


class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "user": UserSerializer(user, context=self.get_serializer_context()).data,
                "token": AuthToken.objects.create(user)[1]
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "user": UserSerializer(user, context=self.get_serializer_context()).data,
                "token": AuthToken.objects.create(user)[1]
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserInfoAPI(views.APIView):

    def get(self, request, format=None):
        try:
            user = User.objects.get(id=request.user.id)
            serializer = UserSerializer(user, many=False)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({"error": "Permission denied"}, status=status.HTTP_401_UNAUTHORIZED)

