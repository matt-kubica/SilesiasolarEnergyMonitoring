
from rest_framework import views, status
from rest_framework.response import Response

from .models import Location, Register, Meter, Host, AssignedMeasurement, Measurement
from .serializers import LocationSerializer, LocationUpdateSerializer, MeterSerializer, HostSerializer, AssignedMeasurementSerializer, MeasurementSerializer, RegisterSerializer
from .permissions import DoesRequestingUserExist, IsLocationOwner


"""
API endpoints for regular users, regular user is only allowed to have all access to Locations and ChosenMeasurements
"""


class LocationAPI(views.APIView):
    permission_classes = [DoesRequestingUserExist, IsLocationOwner, ]


    """ getting all locations of authenticated user """
    def get(self, request, format=None):
        locations = Location.objects.filter(user=request.user.id)
        serializer = LocationSerializer(locations, many=True)
        return Response(serializer.data)

    """ adding new location for authenticated user """
    def post(self, request, format=None):
        serializer = LocationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LocationDetailAPI(views.APIView):
    permission_classes = [DoesRequestingUserExist, ]

    """ getting certain location by id, must belong to user """
    def get(self, request, pk, format=None):
        try:
            location = Location.objects.filter(user=request.user).get(id=pk)
            serializer = LocationSerializer(location, many=False)
            return Response(serializer.data)
        except Location.DoesNotExist:
            return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)

    """ deleting certain location by id, must belong to user """
    def delete(self, request, pk, format=None):
        try:
            location = Location.objects.filter(user=request.user).get(id=pk)
            location.delete()
            return Response({"info": "Location with id {0} has been deleted".format(pk)}, status=status.HTTP_200_OK)
        except Location.DoesNotExist:
            return Response({"error": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)

    """ patching certain location by id, must belong to user """
    def patch(self, request, pk, format=None):
        try:
            location = Location.objects.filter(user=request.user).get(id=pk)
            print(location)
            serializer = LocationUpdateSerializer(location, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Location.DoesNotExist:
            return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)


class AssignedMeasurementAPI(views.APIView):
    permission_classes = [DoesRequestingUserExist, ]


    """ getting all chosen measurements of certain host, user needs to be authenticated """
    def get(self, request, host_id, format=None):

        try:
            host = Host.objects.filter(user=request.user).get(id=host_id)
        except Host.DoesNotExist:
            return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)

        chosen_measurements = AssignedMeasurement.objects.filter(host=host)
        serializer = AssignedMeasurementSerializer(chosen_measurements, many=True)
        return Response(serializer.data)

    """ adding measurements for certain host """
    def post(self, request, host_id, format=None):

        try:
            host = Host.objects.filter(user=request.user).get(id=host_id)
        except Host.DoesNotExist:
            return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)

        # TODO: move this to serializer
        assignments = []
        for measurement in request.data['measurements']:
            assigment = {
                "host": host.id,
                "measurement": measurement
            }
            assignments.append(assigment)

        serializer = AssignedMeasurementSerializer(data=assignments, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # TODO: put and delete



class MeterAPI(views.APIView):
    permission_classes = [DoesRequestingUserExist, ]

    """ getting all available energy meters, user needs to be authenticated event though meter is not directly assigned to user """
    def get(self, request, format=None):
        meters = Meter.objects.all()
        serializer = MeterSerializer(meters, many=True)
        return Response(serializer.data)


class MeasurementDetailByMeterAPI(views.APIView):
    permission_classes = [DoesRequestingUserExist, ]

    """ getting all measurements available for certain meter """
    def get(self, request, meter_id, format=None):
        registers = Register.objects.filter(meter=meter_id)
        if not len(registers):
            return Response({"error": "Cannot find measurements for meter with id {0}".format(meter_id)}, status=status.HTTP_404_NOT_FOUND)

        measurements = []
        for register in registers:
            measurements.append(Measurement.objects.get(name=register.measurement))


        serializer = MeasurementSerializer(measurements, many=True)
        return Response(serializer.data)


class HostAPI(views.APIView):
    permission_classes = [DoesRequestingUserExist, ]

    """ getting all hosts assigned to authenticated user """
    def get(self, request, format=None):
        hosts = Host.objects.filter(user=request.user.id)
        serializer = HostSerializer(hosts, many=True)
        return Response(serializer.data)






