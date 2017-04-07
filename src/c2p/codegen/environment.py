from c2p.ptypes import *
from c2p.grammar.ctypes import *
from typing import Any, List, NamedTuple, Optional, Union
import copy

EnvironmentNode = NamedTuple('EnvironmentNode', [
    ('ctype', CType),
    ('ptype', PType),
    ('address', int),
    ('depth', int),
])

class Environment:
    def __init__(self):
        self.variables = {}
        self.depth = 0
        self.offset = 0

    # Returns a copy of the current Environment, to be used in a deeper scope
    def deepen(self):
        clone = copy.deepcopy(self)
        clone.depth = self.depth + 1
        return clone

    # Allocates a spot of size `size` to the stack for the rest of the scope's duration
    def stack_alloc(self, size : int) -> int:
        addr = self.offset
        self.offset += size
        return addr

    # Registers a variable to the current scope, and all nested scopes within it
    # Overrides existing variables of the same name if they were defined in a higher scope
    def register_variable(self, name : str, ctype : CType) -> None:
        repeatDeclaration = False
        try:
            var = self.variables[name]
            repeatDeclaration = (var.depth == self.depth)
        except:
            pass

        if repeatDeclaration:
            raise ValueError('Repeated declaration of variable {0}'.format(name))

        ptype = ctype.ptype()
        address = self.stack_alloc(ptype.size())
        self.variables[name] = EnvironmentNode(ctype, ptype, address, self.depth)

    def get_address(self, name : str) -> int:
        try:
            var = self.variables[name]
            return var.address
        except KeyError:
            pass
        raise ValueError('Non-existant variable {0}'.format(name))


    # Get the type of a variable in the current scope
    def get_type(self, name : str) -> CType:
        try:
            var = self.variables[name]
            return var.ctype
        except KeyError:
            pass
        raise ValueError('Non-existant variable {0}'.format(name))