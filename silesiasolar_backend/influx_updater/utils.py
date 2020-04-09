from influxdb import InfluxDBClient
from django.conf import settings

from .modbus_client import ModbusClient
from .exceptions import UnknownDatatypeException, ReadError, UnknownFunctioncodeException
from management.models import Meter, Register

def get_db_name(username):
    return '{0}_influxdb'.format(username)


def create_influx_account(username, password):

    client = InfluxDBClient(
        host=settings.DATABASES['influx']['HOST'],
        port=settings.DATABASES['influx']['PORT'],
        username=settings.DATABASES['influx']['ADMIN_USER'],
        password=settings.DATABASES['influx']['ADMIN_PASS']
    )

    db_name = get_db_name(username)
    client.create_user(username, password)
    client.create_database(db_name)
    client.grant_privilege('all', db_name, username)

    # TODO: add retenion policy
    client.close()


def updated_influx():
    meters = Meter.objects.all()
    print(meters)
    influx_client = InfluxDBClient(
        host=settings.DATABASES['influx']['HOST'],
        port=settings.DATABASES['influx']['PORT'],
        username=settings.DATABASES['influx']['ADMIN_USER'],
        password=settings.DATABASES['influx']['ADMIN_PASS']
    )
    # TODO: test connection to influx

    for meter in meters:
        try:
            modbus_client = ModbusClient(host=meter.host, port=meter.port, slave_address=meter.slave_address)
        except ConnectionError as exc:
            print(str(exc) + ', skipping...')
            continue

        registers = Register.objects.filter(meter_type=meter.meter_type)
        print(registers)
        measurements = []

        for register in registers:
            try:
                value = modbus_client.get_value(register_address=register.address, data_type=register.type, function_code=register.function_code)
                measurement = {
                    'measurement': register.measurement,
                    'tags': {
                        'unit': register.unit,
                        'location_id': meter.location.id,
                        'meter_id': meter.id
                    },
                    'fields': {
                        'value': value
                    }
                }
                print(measurement)
                measurements.append(measurement)
            except (UnknownDatatypeException, ReadError, UnknownFunctioncodeException) as exc:
                # TODO: log somehow
                continue

        influx_client.switch_database(get_db_name(meter.user))
        if not influx_client.write_points(measurements):
            # TODO: log
            print('Cannot write to influx')
        measurements.clear()
        modbus_client.close()

    influx_client.close()
    print('Successfully updated influx')





