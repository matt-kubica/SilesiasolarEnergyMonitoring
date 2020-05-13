
from rest_framework import views, status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from accounts.models import User
from accounts.serializers import UserSerializer
from management.models import Location, Meter, Host, Measurement, Register
from management.serializers import LocationSerializer, MeterSerializer, HostSerializer, MeasurementSerializer, RegisterSerializer

# TODO: add more apis, detail etc.

class LocationAPI(views.APIView):
    permission_classes = [IsAdminUser, ]

    """ getting all locations """
    def get(self, request, format=None):
        locations = Location.objects.all()
        serializer = LocationSerializer(locations, many=True)
        return Response(serializer.data)

    """ adding new location """
    def post(self, request, format=None):
        serializer = LocationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LocationDetailAPI(views.APIView):
    permission_classes = [IsAdminUser, ]

    """ getting certain location """
    def get(self, request, pk, format=None):
        try:
            location = Location.objects.get(id=pk)
            serializer = LocationSerializer(location, many=False)
            return Response(serializer.data)
        except Location.DoesNotExist:
            return Response({"error": "Location with id {0} does not exist".format(pk)}, status=status.HTTP_404_NOT_FOUND)

    # TODO: put, delete


class HostAPI(views.APIView):
    permission_classes = [IsAdminUser, ]

    """ getting all hosts """
    def get(self, request, format=None):
        hosts = Host.objects.all()
        serializer = HostSerializer(hosts, many=True)
        return Response(serializer.data)

    """ adding new host """
    def post(self, request, format=None):
        serializer = HostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HostDetailAPI(views.APIView):
    permission_classes = [IsAdminUser, ]

    """ getting certain host """
    def get(self, request, pk, format=None):
        try:
            host = Host.objects.get(id=pk)
            serializer = HostSerializer(host, many=False)
            return Response(serializer.data)
        except Host.DoesNotExist:
            return Response({"error": "Host with id {0} does not exist".format(pk)}, status=status.HTTP_404_NOT_FOUND)

    # TODO: put, delete


class MeterAPI(views.APIView):
    permission_classes = [IsAdminUser, ]

    """ getting all meters """
    def get(self, request, format=None):
        meters = Meter.objects.all()
        serializer = MeterSerializer(meters, many=True)
        return Response(serializer.data)

    """ adding new meter """
    def post(self, request, format=None):
        serializer = MeterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # TODO: put, delete

class RegisterAPI(views.APIView):
    permission_classes = [IsAdminUser, ]

    """ getting all registers """
    def get(self, request, format=None):
        registers = Register.objects.all()
        serializer = RegisterSerializer(registers, many=True)
        return Response(serializer.data)

    """ adding new register """
    def post(self, request, format=None):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # TODO: put, delete


class MeasurementAPI(views.APIView):
    permission_classes = [IsAdminUser, ]

    """ getting all measurements """
    def get(self, request, format=None):
        measurements = Measurement.objects.all()
        serializer = MeasurementSerializer(measurements, many=True)
        return Response(serializer.data)

    """ adding new measurement """
    def post(self, request, format=None):
        serializer = MeasurementSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserAPI(views.APIView):
    permission_classes = [IsAdminUser, ]

    """ getting all users """
    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)



class UserDetailAPI(views.APIView):
    permission_classes = [IsAdminUser, ]

    """ getting certain user info """
    def get(self, request, pk, format=None):
        try:
            user = User.objects.get(id=pk)
            serializer = UserSerializer(user, many=False)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({"error": "User with id {0} does not exist".format(pk)}, status=status.HTTP_404_NOT_FOUND)