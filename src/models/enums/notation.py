from enum import Enum, member


class Notation(Enum):
    """La clase notaciones recopila diferentes notaciones binarias. Al definir el tipo se accede por `.value`."""

    LIL_ENDIAN: member = "little-endian"
    BIG_ENDIAN: member = "big-endian"
    GRAY_CODE: member = "gray-code"
    SIGN_MAGNITUDE: member = "sign-magnitude"
    TWOS_COMPLEMENT: member = "two's-complement"
