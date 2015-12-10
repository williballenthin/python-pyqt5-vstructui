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
        print("error: at least one argument required (path to binary file)")
        return -1

    # vstructui.py /path/to/binary/file "0x0:uint32:first dword" "0x4:uint_2:first word"
    structs = []
    args = list(args)  # we want a list that we can modify
    filename = args.pop(0)

    with open(filename, "rb") as f:
        with contextlib.closing(mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)) as buf:
            for d in args:
                if ":" not in d:
                    raise RuntimeError("invalid structure declaration: {:s}".format(d))

                soffset, _, parser_name = d.partition(":")
                parser_name, _, name = parser_name.partition(":")
                offset = None
                if is_probably_hex(soffset):
                    offset = int(soffset, 0x10)
                else:
                    offset = int(soffset)

                structs.extend(parsers.parse(parser_name, buf, offset, name=name))

            app = QApplication(sys.argv)
            screen = vstructui.VstructViewWidget(parsers, structs, buf)
            screen.show()
            sys.exit(app.exec_())

        
def main():
    sys.exit(_main(*sys.argv[1:]))

if __name__ == "__main__":
    main()
    
