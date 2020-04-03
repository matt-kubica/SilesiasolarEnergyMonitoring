from django.contrib.auth.models import User
from rest_framework import views, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Location, Register, Meter, Node
from .serializers import LocationSerializer, MeterSerializer, NodeSerializer


class LocationAPI(views.APIView):
    # permission_classes = (IsAuthenticated, DoesUserExist)

    def get(self, request, format=None):
        if not User.objects.filter(id=request.user.id):
            return Response({"error": "You're not permitted to get locations"}, status=status.HTTP_403_FORBIDDEN)

        locations = Location.objects.filter(user=request.user.id)
        serializer = LocationSerializer(locations, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        if(request.user.id != request.data['user']):
            return Response({ "error": "Adding location for this user is forbidden" }, status=status.HTTP_403_FORBIDDEN)

        serializer = LocationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)