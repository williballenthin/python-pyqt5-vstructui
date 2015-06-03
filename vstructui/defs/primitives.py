from vstruct.primitives import v_uint8
from vstruct.primitives import v_uint16
from vstruct.primitives import v_uint32
from vstruct.primitives import v_double
from vstruct.primitives import v_float
from vstruct.primitives import v_uint64

from vstructui import VstructParserSet


def vsEntryVstructParser():
    s = VstructParserSet()
    for t in (v_uint8, v_uint16, v_uint32, v_uint64, v_double, v_float, v_uint64):
        s.register_basic_parser(t.__name__, t)
        s.register_basic_parser(t.__name__.lstrip("v_"), t)
    return s

