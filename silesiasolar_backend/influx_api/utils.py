from influxdb import InfluxDBClient
from influxdb.resultset import ResultSet
from influxdb.exceptions import InfluxDBClientError, InfluxDBServerError

from django.conf import settings
from .exceptions import UnknownParameter

import logging
logger = logging.getLogger('influx_api')


GET_CURRENT_QUERY = 'SELECT "value", "unit" FROM {0} WHERE "meter_id" = \'{1}\' ORDER BY "time" DESC LIMIT 1'


def connect_influx():
    try:
        influx_client = InfluxDBClient(
            host=settings.DATABASES['influx']['HOST'],
            port=settings.DATABASES['influx']['PORT'],
            username=settings.DATABASES['influx']['ADMIN_USER'],
            password=settings.DATABASES['influx']['ADMIN_PASS']
        )
        influx_client.request(url='ping', expected_response_code=204)
        return influx_client
    except (ConnectionError, InfluxDBClientError, InfluxDBServerError, Exception) as exc:
        logger.error('Cannot connect to influxdb server on {0}:{1} database: {2}'.format(
            settings.DATABASES['influx']['HOST'], settings.DATABASES['influx']['PORT'], settings.DATABASES['influx']['NAME']))


def influx_get_current(measurement, meter_id):
    client = connect_influx()
    raw = client.query(GET_CURRENT_QUERY.format(measurement, meter_id), epoch="m", database=settings.DATABASES['influx']['NAME']).raw
    if not raw['series']:
        raise UnknownParameter('Measurement \'{0}\' or energy meter with id \'{1}\' not in database.'.format(measurement, meter_id))

    response = {
        'measurement': raw['series'][0]['name'],
        'data': ResultSet.point_from_cols_vals(cols=raw['series'][0]['columns'], vals=raw['series'][0]['values'][0])
    }
    return response





