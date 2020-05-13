from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .exceptions import UnknownParameter
from .utils import influx_get_current
from management.models import Meter


@api_view()
def hello_influx_api(request):
    return Response({"message": "Hello from influx API!"}, status=status.HTTP_200_OK)

@api_view()
def get_current(request):
    meter_id = request.data['meter_id']
    measurement = request.data['measurement']

    if not Meter.objects.filter(user_id=request.user.id).filter(id=meter_id):
        return Response({'error': 'Permission denied for this energy meter.'})

    try:
        return Response(influx_get_current(measurement, meter_id) , status=status.HTTP_200_OK)
    except UnknownParameter as exc:
        return Response({'error': str(exc)}, status=status.HTTP_400_BAD_REQUEST)
