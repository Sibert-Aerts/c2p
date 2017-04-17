from typing import Any

from .base import PInstruction
from ..ptypes import PType, PBoolean


class Ldo(PInstruction):
    """Pushes STORE[q], which has type T."""

    def __init__(self, t: PType, q: int) -> None:
        self.t = t
        self.q = q

    def emit(self) -> str:
        return 'ldo %s %d' % (self.t.letter, self.q)


class Ldc(PInstruction):
    """Pushes a constant q, which has type T."""

    def __init__(self, t: PType, q: Any) -> None:
        self.t = t
        if t == PBoolean:
            self.q = 't' if q else 'f'
        else:
            self.q = q

    def emit(self) -> str:
        return 'ldc %s %s' % (self.t.letter, self.q)


class Ind(PInstruction):
    """Pushes STORE[pop()], which has type T."""

    def __init__(self, t: PType) -> None:
        self.t = t

    def emit(self) -> str:
        return 'ind %s' % self.t.letter


class Sro(PInstruction):
    """Sets STORE[q] to pop(), which has type T."""

    def __init__(self, t: PType, q: int) -> None:
        self.t = t
        self.q = q

    def emit(self) -> str:
        return 'sro %s %d' % (self.t.letter, self.q)


class Sto(PInstruction):
    """Pops (x:T), then pops (j:addr), then sets STORE[j] to x."""

    def __init__(self, t: PType) -> None:
        self.t = t

    def emit(self) -> str:
        return 'sto %s' % self.t.letter


# These are load/store helpers for "difference in nesting depths", using a helper function
#
#     base(p, a) = if p == 0 then a else base(p - 1, STORE[a + 1]).
#
# So basically for p = 0, Lod loads the variable relative to the start of the current frame.


class Lod(PInstruction):
    '''
    Push a value from p frames earlier, at distance q from that frame pointer.
    
    SP := SP + 1; 
    STORE[SP] := STORE[base(p, MP) + q] (of type T)
    '''

    def __init__(self, t: PType, p: int, q: int) -> None:
        self.t = t
        self.p = p
        self.q = q

    def emit(self) -> str:
        return 'lod %s %d %d' % (self.t.letter, self.p, self.q)


class Lda(PInstruction):
    '''
    Push the address of a value from p frames earlier, at distance q from that frame pointer.

    SP := SP + 1; 
    STORE[SP] := base(p, MP) + q
    '''

    def __init__(self, p: int, q: int) -> None:
        self.p = p
        self.q = q

    def emit(self) -> str:
        return 'lda %d %d' % (self.p, self.q)


class Str(PInstruction):
    '''
    Pop a value and store it p frames earlier, at distance q from that frame pointer.

    STORE[base(p, MP) + q] := STORE[SP] (of type T); 
    SP := SP - 1
    '''

    def __init__(self, t: PType, p: int, q: int) -> None:
        self.t = t
        self.p = p
        self.q = q

    def emit(self) -> str:
        return 'str %s %d %d' % (self.t.letter, self.p, self.q)