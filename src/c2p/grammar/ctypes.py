from ..ptypes import PType, PAddress, PBoolean, PCharacter, PInteger, PReal
from typing import Any

class CType:
    def __init__(self) -> None:
        self.class_ = self.__class__

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return not self == other
        return NotImplemented

    def __hash__(self):
       return hash(tuple(sorted(self.__dict__.items())))

    def ptype(self) -> PType:
        raise NotImplementedError()

    def default(self) -> Any:
        raise NotImplementedError()

    def size(self) -> int:
        # Used for array indexing
        return 1

    def __str__(self):
        raise NotImplementedError()

    def ignoreConst(self):
        return self

class CVoid(CType):
    def ptype(self) -> Any:
        raise Exception('void has no PType!')

    def default(self) -> Any:
        raise Exception('void has no default value!')

    def __str__(self):
        return 'void'


class CChar(CType):
    def ptype(self) -> PType:
        return PCharacter

    def default(self) -> Any:
        return '\0'

    def __str__(self):
        return 'char'


class CBool(CType):
    def ptype(self) -> PType:
        return PBoolean

    def default(self) -> Any:
        return False

    def __str__(self):
        return 'bool'


class CInt(CType):
    def ptype(self) -> PType:
        return PInteger

    def default(self) -> Any:
        return 0

    def __str__(self):
        return 'int'


class CFloat(CType):
    def ptype(self) -> PType:
        return PReal

    def default(self) -> Any:
        return 0.0

    def __str__(self):
        return 'float'


class CLayerType(CType):
    def __init__(self, t: CType) -> None:
        super().__init__()
        self.t = t

    def __str__(self):
        return '{0}({1})'.format(self.__class__.__name__, self.t.__str__())

    def ignoreConst(self):
        return self.__class__(self.t.ignoreConst())

class CPointer(CLayerType):
    def ptype(self) -> PType:
        return PAddress

    def default(self) -> Any:
        return 0

    def __str__(self):
        return self.t.__str__() + '*'

class CArray(CLayerType):
    def __init__(self, t: CType, length=None) -> None:
        super().__init__(t)
        self.length = length    # Type: int

    def size(self) -> int:
        if self.length is None:
            return 1
        return self.length * self.t.size()

    def ptype(self) -> PType:
        if self.length is None:
            return PAddress
        return self.t.ptype()

    def default(self) -> Any:
        return 0

    def __str__(self):
        return str(self.t) + '[' + ('' if self.length is None else str(self.length)) + ']'

    def ignoreConst(self):
        return CArray(self.t.ignoreConst(), self.length)

class CConst(CLayerType):
    def ptype(self) -> PType:
        return self.t.ptype()

    def ignoreConst(self):
        return self.t.ignoreConst()

    def default(self) -> Any:
        return self.t.default()

    def __str__(self):
        # TODO I am almost 100% certain this is wrong
        if isinstance(self.t, CPointer):
            return self.t.t.__str__() + '* const'
        else:
            return 'const ' + self.t.__str__()

fromTypeName = { 'void' : CVoid(), 'int' : CInt(), 'float' : CFloat(), 'char' : CChar(), 'bool' : CBool()}