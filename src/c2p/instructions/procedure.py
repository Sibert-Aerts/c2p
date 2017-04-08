from .base import PInstruction
from ..ptypes import PType

# Read this : http://homepages.cwi.nl/~steven/pascal/book/10pcode.html

# base(p,a) = a                             if p == 0
#             base(p – 1, STORE[a + 1])     otherwise

# So essentially base(p, MP) finds the static link,
# I believe in C this is always 0 so who cares what it does

class Mst(PInstruction):
    '''
    p is the depth of the method's definition - the method's use which, in C, is always just 1 I think

    STORE[SP + 2] := base(p, MP)    # static link AKA pointless in C?
    STORE[SP + 3] := MP             # dynamic link AKA pointer to current stack frame
    STORE[SP + 4] := EP             # Max stack size, to prevent stack/heap collission
    SP := SP + 5 

    The parameters can now be evaluated starting from STORE[SP + 1]
    '''
    def __init__(self, p: int) -> None:
        self.p = p

    def emit(self) -> str:
        return 'mst %d' % self.p


class Cup(PInstruction):
    '''
    p is the storage requirement for the method's parameters
    label is the procedure's label

    MP := SP – (p + 4)      # Make a new stack frame?
    STORE[MP + 4] := PC     # Save return address
    PC := label             # Jump to procedure start
    '''

    def __init__(self, p: int, label: str) -> None:
        self.p = p
        self.label = label

    def emit(self) -> str:
        return 'cup %d %s' % (self.p, self.label)


class Ssp(PInstruction):
    '''
    Increase SP by p, to make space for local variables.
    p is the size of the static part of the data area

    SP := MP + p – 1 
    '''
    def __init__(self, p: int) -> None:
        self.p = p

    def emit(self) -> str:
        return 'ssp %d' % self.p


class Sep(PInstruction):
    '''
    Set EP, the frame's maximum size.
    p is max depth of local stack.

    EP := SP + p
    if EP ≥ NP:
        error ('store overflow')
    '''
    def __init__(self, p: int) -> None:
        self.p = p

    def emit(self) -> str:
        return 'sep %d' % self.p


class Ent(PInstruction):
    '''
    Sequence of Ssp and Sep: Make space and check for collission of stack and heap?
    q is data area size,
    p is max depth of local stack. 

    SP := MP + q – 1
    EP := SP + p
    if EP ≥ NP:
        error('store overflow')
    '''
    def __init__(self, p: int, q: int) -> None:
        self.p = p
        self.q = q

    def emit(self) -> str:
        return 'ent %d %d' % (self.p, self.q)


# Returning from functions and procedures

class Retf(PInstruction):
    '''
    Return from a function that produced a result.
    
    SP := MP                    # Function result in local stack
    PC := STORE[MP + 4]         # Return branch
    EP := STORE[MP + 3]         # Restore EP
    if EP ≥ NP:
        error(‘store overflow’)
    '''
    def emit(self) -> str:
        return 'retf'


class Retp(PInstruction):
    '''
    Return from a procedure with no results.

    SP := MP – 1
    PC := STORE[MP + 4]         # Return branch
    EP := STORE[MP + 3]         # Restore EP
    if EP ≥ NP:
        error(‘store overflow’)
    MP := STORE[MP + 2]         # Dynamic link
    '''
    def emit(self) -> str:
        return 'retp'


# Instructions for procedures

class Smp(PInstruction):
    '''
    Make space for parameters...?
    
    MP := SP – (p + 4)
    '''
    def __init__(self, p: int) -> None:
        self.p = p

    def emit(self) -> str:
        return 'smp %d' % self.p


class Cupi(PInstruction):
    '''
    Christ I can't even begin to know.

    STORE[MP + 4] := PC
    PC := STORE[base(p, STORE[MP + 2]) + q] 
    '''
    def __init__(self, p: int, q: int) -> None:
        self.p = p
        self.q = q

    def emit(self) -> str:
        return 'cupi %d %d' % (self.p, self.q)


class Mstf(PInstruction):
    '''
    The opposite of the one above, perhaps, but jesus what the hell.

    STORE[SP + 2] := STORE[base(p, MP) + q + 1]
    STORE[SP + 3] := MP
    STORE[SP + 4] := EP
    SP := SP + 5 
    '''
    def __init__(self, p: int, q: int) -> None:
        self.p = p
        self.q = q

    def emit(self) -> str:
        return 'mstf %d %d' % (self.p, self.q)
