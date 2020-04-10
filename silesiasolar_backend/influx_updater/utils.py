from influxdb import InfluxDBClient
from influxdb.exceptions import InfluxDBClientError, InfluxDBServerError

from django.conf import settings

from .modbus_client import ModbusClient
from .exceptions import UnknownDatatypeException, ReadError, UnknownFunctioncodeException
from management.models import Meter, Register

import logging

logger = logging.getLogger('influx_updater')



def create_influx_account(username, password):

    try:
        client = InfluxDBClient(
            host=settings.DATABASES['influx']['HOST'],
            port=settings.DATABASES['influx']['PORT'],
            username=settings.DATABASES['influx']['ADMIN_USER'],
            password=settings.DATABASES['influx']['ADMIN_PASS']
        )
        # test connection
        client.request(url='ping', expected_response_code=204)

        client.create_user(username, password)
        client.grant_privilege('all', settings.DATABASES['influx']['NAME'], username)
        # TODO: add retention policy
        client.close()
    except (ConnectionError, InfluxDBClientError, InfluxDBServerError, Exception) as exc:
        logger.error('Cannot connect to influxdb server -> {0}:{1}'.format(settings.DATABASES['influx']['HOST'],
                                                                            settings.DATABASES['influx']['PORT']))
        logger.error('Influx user and database could not be created for {0}'.format(username))




def update_influx():
    meters = Meter.objects.all()
    logger.info('Meters to update: {0}'.format(len(meters)))

    try:
        influx_client = InfluxDBClient(
            host=settings.DATABASES['influx']['HOST'],
            port=settings.DATABASES['influx']['PORT'],
            username=settings.DATABASES['influx']['ADMIN_USER'],
            password=settings.DATABASES['influx']['ADMIN_PASS']
        )
        influx_client.switch_database(settings.DATABASES['influx']['NAME'])
        influx_client.request(url='ping', expected_response_code=204)
    except (ConnectionError, InfluxDBClientError, InfluxDBServerError, Exception) as exc:
        logger.error('Cannot connect to influxdb server on {0}:{1} database: {2}'.format(
            settings.DATABASES['influx']['HOST'], settings.DATABASES['influx']['PORT'], settings.DATABASES['influx']['NAME']))
        logger.error('Data won\'t be retrieved from meters...')
        return


    for meter in meters:
        try:
            modbus_client = ModbusClient(host=meter.host, port=meter.port, slave_address=meter.slave_address)
        except ConnectionError as exc:
            logger.warning('Cannot connect to meter {0}:{1}, skipping...'.format(meter.host, meter.port))
            continue

        registers = Register.objects.filter(meter_type=meter.meter_type)
        measurements = []

        for register in registers:
            try:
                value = modbus_client.get_value(register_address=register.address, data_type=register.type, function_code=register.function_code)
                measurement = {
                    'measurement': register.measurement,
                    'tags': {
                        'unit': register.unit,
                        'user_id': meter.user.id,
                        'location_id': meter.location.id,
                        'meter_id': meter.id
                    },
                    'fields': {
                        'value': value
                    }
                }
                measurements.append(measurement)
            except (UnknownDatatypeException, ReadError, UnknownFunctioncodeException) as exc:
                logger.warning('Cannot read {0} register, provided function_code = {1}, data_type = {2}\nException message:\n{3}'.format(
                    register.address, register.function_code, register.type, str(exc)))
                continue

        if not influx_client.write_points(measurements, time_precision='m', protocol='json'):
            logger.error('Cannot write data points from {0} to influx'.format(meter))
        else:
            logger.debug('Updated influx with data from {0}\nData:\n{1}'.format(meter, measurements))
        measurements.clear()
        modbus_client.close()

    influx_client.close()





