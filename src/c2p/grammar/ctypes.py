from ..ptypes import PType, PAddress, PBoolean, PCharacter, PInteger, PReal
from typing import Any, Optional

class CType:
    def __init__(self) -> None:
        self.class_ = self.__class__

    def __eq__(self, other):
        return isinstance(other, self.__class__)

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
       return hash(tuple(sorted(self.__dict__.items())))

    def equivalent(self, other):
        return self.ignoreConst() == other.ignoreConst()

    def promotes_to(self, other : 'CType') -> bool:
        '''Test whether this type can be promoted to the other type without loss.'''
        s = self.ignoreConst().__class__
        o = other.ignoreConst().__class__
        if not (s in numericOrder and o in numericOrder):
            return False
        return numericOrder.index(s) <= numericOrder.index(o)

    def demotes_to(self, other : 'CType') -> bool:
        '''Test whether converting to the given type is possible and causes loss.'''
        s = self.ignoreConst().__class__
        o = other.ignoreConst().__class__
        if not (s in numericOrder and o in numericOrder):
            return False
        return numericOrder.index(s) >= numericOrder.index(o)

    def common_promote(self, other : 'CType') -> Optional['CType']:
        '''
        Finds the smallest type that both can be promoted to without loss.
        Returns None if no such type exists.
        '''
        if self.promotes_to(other):
            return other.ignoreConst()
        elif other.promotes_to(self):
            return self.ignoreConst()
        return None

    def ptype(self) -> PType:
        raise NotImplementedError()

    def default(self) -> Any:
        raise NotImplementedError()

    def size(self) -> int:
        # Used for array indexing
        return 1

    def __str__(self):
        raise NotImplementedError()

    def _str(self, inner):
        return str(self) + ' ' + inner

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

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.t == other.t

    def __str__(self):
        return self._str('').rstrip()

    def ignoreConst(self):
        return self.__class__(self.t.ignoreConst())

class CPointer(CLayerType):
    def ptype(self) -> PType:
        return PAddress

    def default(self) -> Any:
        return 0

    def promotes_to(self, other : 'CType') -> bool:
        '''Test whether this type can be promoted to the other type without loss.'''
        o = other.ignoreConst()
        return isinstance(o, CPointer) and self.t.equivalent(o.t)

    def _str(self, inner):
        if isinstance(self.t, CConst):
            inner = '* const ' + inner
        else:
            inner = '*' + inner
        if isinstance(self.t.ignoreConst(), CArray):
            inner = '(' + inner + ')'
        return self.t._str(inner)

class CArray(CLayerType):
    def __init__(self, t: CType, length : int) -> None:
        super().__init__(t)
        self.length = length

    def promotes_to(self, other : 'CType') -> bool:
        '''Test whether this type can be promoted to the other type without loss.'''
        return isinstance(other.ignoreConst(), (CArray, CPointer)) and self.t.equivalent(other.ignoreConst().t)

    def size(self) -> int:
        return self.length * self.t.size()

    def ptype(self) -> PType:
        return PAddress

    def default(self) -> Any:
        return 0

    def _str(self, inner):
        return self.t._str(inner + '[' + str(self.length) + ']')

    def ignoreConst(self):
        return CArray(self.t.ignoreConst(), self.length)

class CConst(CLayerType):
    def ptype(self) -> PType:
        return self.t.ptype()

    def ignoreConst(self):
        return self.t.ignoreConst()

    def promotes_to(self, other : 'CType') -> bool:
        return self.t.promotes_to(other)

    def default(self) -> Any:
        return self.t.default()

    def _str(self, inner):
        if not isinstance(self.t, CLayerType):
            return 'const ' + str(self.t) + ' ' + inner
        else:
            return self.t._str(inner)

fromTypeName = { 'void' : CVoid(), 'int' : CInt(), 'float' : CFloat(), 'char' : CChar(), 'bool' : CBool()}

numericOrder = [CBool, CChar, CInt, CFloat]