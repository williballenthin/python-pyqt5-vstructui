import os
import sys
import imp
import mmap
import contextlib

from PyQt5.QtWidgets import QApplication

from vstruct import VStruct
from vstruct import VArray
from vstruct.primitives import v_prim
from vstruct.primitives import v_number
from vstruct.primitives import v_bytes
from vstruct.primitives import v_uint8
from vstruct.primitives import v_uint16
from vstruct.primitives import v_uint32

from vstructui.vstruct_parser import ComposedParser
from vstructui.vstruct_parser import VstructInstance

import vstructui


# TODO: use pkg_resources
defspath = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "defs")
def get_parsers(defspath=defspath):
    parsers = ComposedParser()
    for filename in os.listdir(defspath):
        if not filename.endswith(".py"):
            continue
        deffilepath = os.path.join(defspath, filename)
        mod = imp.load_source("vstruct_parser", deffilepath)
        if not hasattr(mod, "vsEntryVstructParser"):
            continue
        parser = mod.vsEntryVstructParser()
        parsers.add_parser(parser)
    return parsers


_HEX_ALPHA_CHARS = set(list("abcdefABCDEF"))
def is_probably_hex(s):
    if s.startswith("0x"):
        return True

    for c in s:
        if c in _HEX_ALPHA_CHARS:
            return True

    return False


def _main(*args):
    parsers = get_parsers()
    buf = ""
    structs = ()
    filename = None
    if len(args) == 0:
        b = []
        for i in range(0x100):
            b.append(i)
        buf = bytearray(b)

        class TestStruct(VStruct):
            def __init__(self):
                VStruct.__init__(self)
                self.a = v_uint8()
                self.b = v_uint16()
                self.c = v_uint32()
                self.d = v_uint8()
                self.e = VArray((v_uint32(), v_uint32(), v_uint32(), v_uint32()))

        t1 = TestStruct()
        t1.vsParse(buf, offset=0x0)

        t2 = TestStruct()
        t2.vsParse(buf, offset=0x40)
        structs = (VstructInstance(0x0, t1, "t1"), VstructInstance(0x40, t2, "t2"))
    else:
        # vstructui.py /path/to/binary/file "0x0:uint32:first dword" "0x4:uint_2:first word"
        structs = []
        args = list(args)  # we want a list that we can modify
        filename = args.pop(0)

        for d in args:
            if ":" not in d:
                raise RuntimeError("invalid structure declaration: {:s}".format(d))

            soffset, _, parser_name = d.partition(":")
            name = ""
            if ":" in parser_name:
                parser_name, _, name = parser_name.partition(":")
            offset = None
            if is_probably_hex(soffset):
                offset = int(soffset, 0x10)
            else:
                offset = int(soffset)

            structs.extend(parsers.parse(parser_name, buf, offset, name=name))

    def doit(buf):
        app = QApplication(sys.argv)
        screen = vstructui.VstructViewWidget(parsers, structs, buf)
        screen.show()
        sys.exit(app.exec_())

    if filename is not None:
        with open(filename, "rb") as f:
            with contextlib.closing(mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)) as buf:
                doit(buf)
    else:
        doit(buf)
        
def main():
    sys.exit(_main(*sys.argv[1:]))

if __name__ == "__main__":
    main()
    
