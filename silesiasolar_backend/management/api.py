from django.contrib.auth.models import User
from rest_framework import views, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from .models import Location, Register, Meter, Node
from .serializers import LocationSerializer, MeterSerializer, NodeSerializer
from .permissions import DoesRequestingUserExist, IsOwner


# api endpoint to get information about locations of logged user or to post new location of logged user
class UserLocationAPI(views.APIView):
    permission_classes = [DoesRequestingUserExist, IsOwner, ]
    # TODO: additional permissions ?
    # TODO: put and delete

    def get(self, request, format=None):
        locations = Location.objects.filter(user=request.user.id)
        serializer = LocationSerializer(locations, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = LocationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserMeterAPI(views.APIView):
    permission_classes = [DoesRequestingUserExist, ]
    # TODO: additional permissions ?


    def get(self, request, format=None):
        meters = Meter.objects.filter(user=request.user.id)
        serializer = MeterSerializer(meters, many=True)
        return Response(serializer.data)


class AdminMeterAPI(views.APIView):
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


