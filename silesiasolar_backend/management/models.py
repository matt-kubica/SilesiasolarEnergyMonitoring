from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import User
from .utils import DataTypes, FunctionCodes, MeterTypes, MeasurementTypes

zip_code_regex = '^[0-9]{2}-[0-9]{3}$'
ip_regex = '^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'

class Location(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    street = models.CharField(max_length=32, null=False)
    number = models.CharField(max_length=8, null=False)
    city = models.CharField(max_length=32, null=False)
    zip_code = models.CharField(max_length=6, null=False, validators=[RegexValidator(regex=zip_code_regex)])
    coord_x = models.FloatField(null=True, blank=True)
    coord_y = models.FloatField(null=True, blank=True)

    def __str__(self):
        return 'city: {0}, street: {1}, number: {2}'.format(self.city, self.street, self.number)

    class Meta:
        unique_together = ('street', 'number', 'city',)


class Meter(models.Model):
    name = models.CharField(max_length=64, null=False, unique=True)
    type = models.PositiveIntegerField(choices=MeterTypes.choices(), null=False)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('name', 'type', )


class Measurement(models.Model):
    measurement = models.CharField(max_length=64, null=False, primary_key=True)
    type = models.PositiveIntegerField(choices=MeasurementTypes.choices(), null=False)

    def __str__(self):
        return self.measurement


class Host(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    meter = models.ForeignKey(Meter, on_delete=models.CASCADE)

    ip = models.CharField(max_length=64, null=False)
    port = models.PositiveIntegerField(null=False)
    slave_address = models.PositiveSmallIntegerField(null=False)
    description = models.CharField(max_length=128)

    def __str__(self):
        return 'host: {0}:{1}:{2}'.format(self.ip, self.port, self.slave_address)

    class Meta:
        unique_together = ('ip', 'port', 'slave_address', )


class ChosenMeasurements(models.Model):
    host = models.ForeignKey(Host, on_delete=models.CASCADE)
    measurement = models.ForeignKey(Measurement, on_delete=models.CASCADE)

    def __str__(self):
        return 'host: {0}, measurement: {1}'.format(self.host, self.measurement)

    class Meta:
        unique_together = ('host', 'measurement', )


class Register(models.Model):
    meter = models.ForeignKey(Meter, on_delete=models.CASCADE)
    measurement = models.ForeignKey(Measurement, on_delete=models.CASCADE)

    address = models.PositiveIntegerField(null=False)
    unit = models.CharField(max_length=8, blank=True, null=True)
    type = models.PositiveIntegerField(choices=DataTypes.choices(), null=False)
    function_code = models.PositiveIntegerField(choices=FunctionCodes.choices(), null=False)

    def __str__(self):
        return 'meter: {0}, measurement: {1}, address: {2}'.format(self.meter)

    class Meta:
        unique_together = ('meter', 'measurement', )

