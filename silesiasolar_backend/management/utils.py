from enum import IntEnum

class CustomEnum(IntEnum):
    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class DataTypes(CustomEnum):
    INT = 1
    LONG = 2
    FLOAT = 3


class FunctionCodes(CustomEnum):
    READ_HOLDING_REGISTERS = 3
    READ_INPUT_REGISTERS = 4


class MeterTypes(CustomEnum):
    SINGLE_DIRECTIONAL = 1
    BI_DIRECTIONAL = 2


class MeasurementTypes(CustomEnum):
    CURRENT = 1
    HISTORICAL = 2