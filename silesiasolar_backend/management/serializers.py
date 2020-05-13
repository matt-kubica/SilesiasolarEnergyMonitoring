from rest_framework import serializers
from .models import Location, Meter, Register, Host, Measurement, ChosenMeasurements

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class HostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Host
        fields = '__all__'

    def validate(self, attrs):
        # check if user is owner of the location
        if attrs['location'] not in Location.objects.filter(user=attrs['user']):
            raise serializers.ValidationError({"structural_error": "Meter and its location must belong to same user"})
        return attrs


class MeterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meter
        fields ='__all__'


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Register
        fields = '__all__'


class MeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = '__all__'


class ChosenMeasurementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChosenMeasurements
        fields = '__all__'


