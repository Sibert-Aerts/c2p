from c2p.ptypes import *
from c2p.grammar.ctypes import *
from typing import Any, Dict, Iterable, List, NamedTuple, Optional, Union
from c2p.instructions.branch import Label
import copy


VariableRecord = NamedTuple('VariableRecord', [
    ('ctype', CType),
    ('ptype', PType),
    ('address', int),
    ('depth', int),
    ('isGlobal', bool)
])

FunctionRecord = NamedTuple('FunctionRecord', [
    ('returnType', CType),
    ('signature', List[CType]),
    ('label', Label),
])

class Scope:
    '''A mapping of symbols (names) to variable/function records, which may
    itself have parent or child scopes.'''
    def __init__(self, parent: Optional['Scope']) -> None:
        self.parent = parent
        self.children = [] # type: List[Scope]
        self.symbols = {} # type: Dict[str, Union[VariableRecord, FunctionRecord]]
        # varSpace is the amount of space the variables defined in this scope take up
        # varSpace is NOT an address
        self.varSpace = 0

        if parent is None:
            self.depth = 0
        else: # Calculate depth, append self to the parent
            self.depth = parent.depth + 1
            self.parent.children.append(self)

    def frame_var_space(self) -> int:
        '''
        Get the total space of all variables reachable by this scope (upwards recursive),
        that are stored in the current frame (so no globals).
        Used to help determine the address for variables defined in a Statement inside a function.
        '''
        varSpace = 0
        scope = self
        while scope.depth != 0:
            varSpace += node.varSpace
            scope = scope.parent
        return varSpace

    def max_var_space(self) -> int:
        '''
        Get the maximum amount of variable space this scope uses at a single time (downwards recusive).
        Used to determine the minimum amount of space that needs to be set aside on the stack before the
        stack can be used for evaluating expressions.
        '''
        childMaxVarSpace = max((c.max_var_space() for c in self.children), default=0)
        return childMaxVarSpace + self.varSpace

    def find(self, name:str) -> Union[VariableRecord, FunctionRecord]:
        '''Search upwards through the tree to find the first symbol by the given name.

        Returns None if the symbol is not found.'''
        scope = self
        while scope:
            if name in scope.symbols:
                return scope.symbols[name]
            scope = scope.parent
        return None

    def _alloc(self, size: int) -> int:
        addr = self.frame_var_space()
        self.varSpace += size
        return addr

    def _get_variable(self, name: str) -> VariableRecord:
        variable = self.find(name)
        if not variable:
            raise ValueError('Use of undefined variable "{}"'.format(name))
        if isinstance(variable, FunctionRecord):
            raise ValueError('Attempted to use symbol "{}" as a variable when it is a function.'.format(name))
        return variable

    def _get_function(self, name: str) -> FunctionRecord:
        function = self.scope.find(name)
        if not function:
            raise ValueError('Use of undefined function "{}"'.format(name))
        if isinstance(function, VariableRecord):
            raise ValueError('Attempted to use symbol "{}" as a function when it is a variable.'.format(name))
        return function

    def _register_variable(self, name: str, ctype: CType) -> None:
        # Check if the symbol is already defined in the current scope
        if name in self.symbols:
            raise ValueError('Repeated declaration of symbol "{}"'.format(name))

        # Make a new variable record and register it to the current scope.
        ptype = ctype.ptype()
        isGlobal = (self.depth == 0)
        # Address works differently for global/local variables
        # TODO: or does it really?
        address = self.alloc(ptype.size())
        if not isGlobal:
            address += 5

        print('registered var {} at depth {} at address {}'.format(name, self.depth, address))
        self.symbols[name] = VariableRecord(ctype, ptype, address, self.depth, isGlobal)

    def _register_function(self, name: str, returnType: CType, signature: List[CType]) -> Label:
        assert self.depth == 0, 'register_function not at global scope'

        # Check if the symbol is already defined in the current scope
        if name in self.symbols:
            raise ValueError('Repeated declaration of symbol "{}"'.format(name))

        # Make a function record and register it
        label = Label('f_{}'.format(name))
        self.symbols[name] = FunctionRecord(returnType, signature, label)
        return label

class Environment:
    '''Manages a Scope.'''

    def __init__(self):
        self.scope = Scope(None)

    def deepen(self):
        '''Deepens the symbol scope.'''
        newScope = Scope(self.scope)
        self.scope = newScope

    def undeepen(self):
        '''Undeepens the symbol scope: All symbols defined in this level drop out of scope.'''
        self.scope = self.scope.parent

    def alloc(self, size: int) -> int:
        '''Allocates a spot of size `size` to the current scope, returning its address.'''
        return self.scope._alloc(size)

    def get_variable(self, name: str) -> VariableRecord:
        '''Retrieve a variable record from this scope or above, or throw a ValueError.'''
        return self.scope._get_variable(name)

    def get_function(self, name: str) -> FunctionRecord:
        '''Retrieve a function record from this scope or above, or throw a ValueError.'''
        return self.scope._get_function(name)

    def register_variable(self, name: str, ctype: CType) -> None:
        '''Registers a variable to the current scope.'''
        return self.scope._register_variable(name, ctype)

    def register_function(self, name: str, returnType: CType, signature: List[CType]) -> Label:
        '''Registers a function to the (global) scope and get its label.'''
        return self.scope._register_function(name, returnType, signature)
