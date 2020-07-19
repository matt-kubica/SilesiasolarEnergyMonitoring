from pymodbus.client.sync import ModbusTcpClient
from .exceptions import UnknownDatatypeException, UnknownFunctioncodeException, ReadError
from management.utils import DataTypes, FunctionCodes
import numpy as np

class ModbusClient(ModbusTcpClient):

    def __init__(self, host, port, subordinate_address):
        self.host = host
        self.port = port
        self.subordinate_address = subordinate_address
        ModbusTcpClient.__init__(self, host=host, port=port)
        if not self.connect():
            raise ConnectionError('Cannot connect to {0}:{1}'.format(host, port))

    def convert(self, registers, data_type):
        if data_type == DataTypes.INT:
            return registers[0]
        elif data_type == DataTypes.FLOAT:
            tmp = np.array(registers, np.int16)
            tmp.dtype = np.float32
            return tmp[0]
        else:
            tmp = np.array(registers, np.int16)
            tmp.dtype = np.int32
            return tmp[0]

    def get_value(self, register_address, function_code, data_type):
        response = None
        bytes_count = None

        if data_type in (DataTypes.LONG, DataTypes.FLOAT):
            bytes_count = 2
        elif data_type in (DataTypes.INT, ):
            bytes_count = 1
        else:
            raise UnknownDatatypeException('Unknown data type with id: {0}'.format(data_type))

        if function_code == FunctionCodes.READ_INPUT_REGISTERS:
            response = self.read_input_registers(address=register_address, count=bytes_count, unit=self.subordinate_address)
        elif function_code == FunctionCodes.READ_HOLDING_REGISTERS:
            response = self.read_input_registers(address=register_address, count=bytes_count, unit=self.subordinate_address)
        else:
            raise UnknownFunctioncodeException('Unknown function code: {0}'.format(function_code))

        if response.isError():
            raise ReadError('Cannot get value from register: {0}, subordinate_address: {1}'.format(register_address, self.subordinate_address))

        return self.convert(response.registers, data_type)

