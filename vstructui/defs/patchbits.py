from vstruct import VStruct
from vstruct.primitives import v_bytes
from vstruct.primitives import v_uint32
from vstruct.primitives import v_wstr

from vstructui import BasicVstructParser


# from: https://github.com/evil-e/sdb-explorer/blob/master/sdb.h
class PATCHBITS(VStruct):
    def __init__(self):
        VStruct.__init__(self)
        opcode = v_uint32()
        action_size = v_uint32()
        pattern_size = v_uint32()
        rva = v_uint32()
        unknown = v_uint32()
        module_name = v_wstr(size=32)
        pattern = v_bytes(size=0)

    def pcb_pattern_size(self):
        self["pattern"].vsSetLength(self.pattern_size)


def vsEntryVstructParser():
    return BasicVstructParser((PATCHBITS,))

