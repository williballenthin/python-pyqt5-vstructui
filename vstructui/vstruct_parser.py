from abc import ABCMeta
from abc import abstractproperty
from abc import abstractmethod
from functools import partial
from collections import namedtuple


VstructInstance = namedtuple("VstructInstance", ["offset", "instance", "name"])

class VstructParserInterface(object):
    __metaclass__ = ABCMeta

    @abstractproperty
    def parser_names(self):
        """
        :rtype: Iterable[str]
        """
        raise NotImplementedError()

    @abstractmethod
    def parse(self, parser_name, buf, offset, name=None):
        """
        :rtype: Iterable[VstructInstance]
        """
        raise NotImplementedError()

    def __repr__(self):
        return "VstructParser(for: {:s})".format(", ".join(self.parser_names))

    def __str__(self):
        return repr(self)


class VstructParser(VstructParserInterface):
    def __init__(self):
        super(VstructParser, self).__init__()
        self._parsers = {}

    @staticmethod
    def _basic_parse(Klass, buf, offset, name=None):
        v = Klass()
        v.vsParse(buf, offset=offset)
        return (VstructInstance(offset, v, name=name), )

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
            self.register_basic_parser(klass.__name__, klass)


class ParserSet(VstructParserInterface):
    def __init__(self, parsers=None):
        super(ParserSet, self).__init__()
        self._parsers = []  # type: VstructParserInterface
        if parsers is not None:
            self._parsers = parsers

    @property
    def parser_names(self):
        names = []
        for parser in self._parsers:
            names.extend(parser.parser_names)
        return names

    def parse(self, parser_name, buf, offset, name=None):
        for parser in self._parsers:
            if parser_name in parser.parser_names:
                return parser.parse(parser_name, buf, offset, name=name)
        raise IndexError()

    def add_parser(self, parser):
        """
        :type parser: VstructParserInterface
        """
        self._parsers.append(parser)

