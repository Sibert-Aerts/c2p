from ..ptypes import PType, PAddress, PBoolean, PCharacter, PInteger, PReal

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

    def size(self) -> int:
        # Used for array indexing
        return 1

    def __repr__(self):
        return self.__class__.__name__

    def ignoreConst(self):
        return self

class CVoid(CType):
    def ptype(self) -> PType:
        raise ValueError('void has no PType!')


class CChar(CType):
    def ptype(self) -> PType:
        return PCharacter


class CBool(CType):
    def ptype(self) -> PType:
        return PBoolean


class CInt(CType):
    def ptype(self) -> PType:
        return PInteger


class CFloat(CType):
    def ptype(self) -> PType:
        return PReal


class CLayerType(CType):
    def __init__(self, t: CType) -> None:
        super().__init__()
        self.t = t

    def __repr__(self):
        return '{0}({1})'.format(self.__class__.__name__, self.t.__repr__())

    def ignoreConst(self):
        return self.__class__(self.t.ignoreConst())

class CPointer(CLayerType):
    def ptype(self) -> PType:
        return PAddress

class CArray(CLayerType):
    def __init__(self, t: CType, length=None) -> None:
        super().__init__(t)
        self.length = length    # Type: int

    def __repr__(self):
        return '{}[{}]({})'.format(self.__class__.__name__, self.length, self.t.__repr__())

    def size(self) -> int:
        if self.length:
            return self.length * self.t.size()
        else:
            raise ValueError('Attempted to get length of array with non-specified length.')

    def ptype(self) -> PType:
        return PAddress

class CConst(CLayerType):
    def ptype(self) -> PType:
        return self.t.ptype()

    def ignoreConst(self):
        return self.t.ignoreConst()

fromTypeName = { 'void' : CVoid(), 'int' : CInt(), 'float' : CFloat(), 'char' : CChar()}