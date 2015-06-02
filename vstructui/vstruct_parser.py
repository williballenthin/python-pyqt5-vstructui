from functools import partial
from collections import namedtuple


VstructInstance = namedtuple("VstructInstance", ["offset", "instance", "name"])


class VstructParser(object):
    def __init__(self):
        super(VstructParser, self).__init__()
        self._parsers = {}

    @staticmethod
    def _basic_parse(Klass, buf, offset, name=None):
        v = Klass()
        v.vsParse(buf, offset=offset)
        return (VstructInstance(offset, v, name=name))

    def register_basic_parser(self, name, Klass):
        self._parsers[name] = partial(self._basic_parse, Klass)

    @property
    def parser_names(self):
        return self._parsers.keys()

    def parse(self, parser_name, buf, offset, name=None):
        return self._parsers[parser_name](buf, offset, name=name)


class BasicVstructParser(VstructParser):
    """
    so we can do something like:

        class FOO(VStruct)...
        class BAR(VStruct)...

        def vsEntryVstructParser():
            return BasicVstructParser((FOO, BAR))
    """
    def __init__(self, vstruct_klasses):
        super(BasicVstructParser, self).__init__()
        for klass in vstruct_klasses:
            self.register_basic_parser(klass.__class__.__name__, klass)
