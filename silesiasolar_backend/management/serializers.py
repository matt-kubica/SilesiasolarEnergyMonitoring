from rest_framework import serializers
from .models import Location, Meter, Register, Node
from .utils import NodeTypes

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class MeterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meter
        fields = '__all__'

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Register
        fields = '__all__'

class NodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = '__all__'

    def validate(self, data):
        if data['type'] == NodeTypes.FORK and data['meter'] != None:
            raise serializers.ValidationError({"structural error": "Meter cannot be assigned to the fork type node." })
        if data['type'] == NodeTypes.METER and data['meter'] == None:
            raise  serializers.ValidationError({"structural error": "Meter must be assigned to the meter type node." })
        if data['meter'] != None and self.check_if_meter_assigned(data['meter']):
            raise serializers.ValidationError({"structural error": "Meter of id {0} is already assigned to another node.".format(data['meter'])})
        return data

    @staticmethod
    def check_if_meter_assigned(meter):
        meter = Meter.objects.get(pk=meter.id)
        return meter.assigned
