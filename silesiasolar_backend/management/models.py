from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import User
from .utils import DataTypes, FunctionCodes, NodeTypes, MeterTypes

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


class Meter(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    host = models.CharField(max_length=15, null=False, validators=[RegexValidator(regex=ip_regex)])
    port = models.PositiveIntegerField(null=False)
    slave_address = models.PositiveSmallIntegerField(null=False)
    type = models.PositiveIntegerField(choices=MeterTypes.choices())
    model = models.CharField(max_length=30, unique=False)
    assigned = models.BooleanField(default=False)


class Node(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    meter = models.ForeignKey(Meter, blank=True, null=True, on_delete=models.CASCADE)
    type = models.PositiveIntegerField(choices=NodeTypes.choices())
    nodes_connected = models.ManyToManyField('self', blank=True)
    main = models.BooleanField(default=False)
    description = models.CharField(max_length=100)


class Register(models.Model):
    meter_id = models.CharField(max_length=30, unique=False)
    address = models.PositiveIntegerField(null=False)
    measurement = models.CharField(max_length=30, null=False)
    unit = models.CharField(max_length=5, blank=True, null=True)
    type = models.PositiveIntegerField(choices=DataTypes.choices(), null=False)
    function_code = models.PositiveIntegerField(choices=FunctionCodes.choices(), null=False)
    sf_address = models.PositiveIntegerField(blank=True, null=True)
    sf_constant = models.FloatField(default=1)

