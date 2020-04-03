from knox.auth import User
from rest_framework import views, status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from accounts.serializers import UserSerializer
from management.models import Location, Meter
from management.serializers import LocationSerializer, MeterSerializer

# TODO: add more apis, detail etc.

class LocationAPI(views.APIView):
    permission_classes = [IsAdminUser, ]

    def get(self, request, format=None):
        locations = Location.objects.all()
        serializer = LocationSerializer(locations, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = LocationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MeterAPI(views.APIView):
    permission_classes = [IsAdminUser, ]
    # TODO: put and delete

    def get(self, request, format=None):
        meters = Meter.objects.all()
        serializer = MeterSerializer(meters, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = MeterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserAPI(views.APIView):
    permission_classes = [IsAdminUser, ]

    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    # TODO: post, put, delete

class DetailUserAPI(views.APIView):
    permission_classes = [IsAdminUser, ]

    def get(self, request, pk, format=None):
        try:
            user = User.objects.get(id=pk)
            serializer = UserSerializer(user, many=False)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({"error": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)