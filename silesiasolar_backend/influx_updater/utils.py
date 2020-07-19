from influxdb import InfluxDBClient
from influxdb.exceptions import InfluxDBClientError, InfluxDBServerError

from django.conf import settings

from .modbus_client import ModbusClient
from .exceptions import UnknownDatatypeException, ReadError, UnknownFunctioncodeException, InfluxUserNotCreated
from management.models import Host, Register, AssignedMeasurement

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
        raise InfluxUserNotCreated




def update_influx():
    hosts = Host.objects.all()
    logger.info('Hosts to update: {0}'.format(len(hosts)))

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


    for host in hosts:
        try:
            modbus_client = ModbusClient(host=host.ip, port=host.port, subordinate_address=host.subordinate_address)
        except ConnectionError as exc:
            logger.warning('Cannot connect to host {0}:{1}, skipping...'.format(host.ip, host.port))
            continue

        data_points = []
        for assigned_measurement in AssignedMeasurement.objects.filter(host=host):
            register = Register.objects.get(measurement=assigned_measurement.measurement, meter=host.meter)
            try:
                value = modbus_client.get_value(register_address=register.address, data_type=register.type, function_code=register.function_code)
                data_point = {
                    'measurement': register.measurement.name,
                    'tags': {
                        'unit': register.unit,
                        'user_id': host.user.id,
                        'location_id': host.location.id,
                        'host': host.id
                    },
                    'fields': {
                        'value': value
                    }
                }
                data_points.append(data_point)
            except (UnknownDatatypeException, ReadError, UnknownFunctioncodeException) as exc:
                logger.warning('Cannot read {0} register, provided function_code = {1}, data_type = {2}\nException message:\n{3}'.format(
                    register.address, register.function_code, register.type, str(exc)))
                continue

        if not data_points:
            logger.warning('No measurements assigned to {0}'.format(host))
        else:
            if not influx_client.write_points(data_points, time_precision='m', protocol='json'):
                logger.error('Cannot write data points from {0} to influx'.format(host))
            else:
                logger.debug('Updated influx with data from {0}\nData:\n{1}'.format(host, data_points))

        data_points.clear()
        modbus_client.close()

    influx_client.close()





