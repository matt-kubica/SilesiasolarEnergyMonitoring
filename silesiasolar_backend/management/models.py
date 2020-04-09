from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import User
from .utils import DataTypes, FunctionCodes

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

    class Meta:
        unique_together = ('street', 'number', 'city',)


class Meter(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    # host = models.CharField(max_length=15, null=False, validators=[RegexValidator(regex=ip_regex)])
    host = models.CharField(max_length=32, null=False)
    port = models.PositiveIntegerField(null=False)
    slave_address = models.PositiveSmallIntegerField(null=False)

    meter_type = models.CharField(max_length=32, unique=False)
    assigned = models.BooleanField(default=False)
    description = models.CharField(max_length=128)

    def __str__(self):
        return '{0}:{1}:{2}'.format(self.host, self.port, self.slave_address)

    class Meta:
        unique_together = ('host', 'port', 'slave_address', )

class Register(models.Model):
    # TODO: try to apply many to many relation between meter and register models
    meter_type = models.CharField(max_length=32, unique=False)
    address = models.PositiveIntegerField(null=False)
    measurement = models.CharField(max_length=64, null=False)
    unit = models.CharField(max_length=8, blank=True, null=True)
    type = models.PositiveIntegerField(choices=DataTypes.choices(), null=False)
    function_code = models.PositiveIntegerField(choices=FunctionCodes.choices(), null=False)
    sf_address = models.PositiveIntegerField(blank=True, null=True)
    sf_constant = models.FloatField(default=1)

