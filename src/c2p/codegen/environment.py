from c2p.ptypes import *
from c2p.grammar.ctypes import *
from typing import Any, Dict, List, NamedTuple, Optional, Union
from c2p.instructions.branch import Label
import copy


VariableRecord = NamedTuple('VariableRecord', [
    ('ctype', CType),
    ('ptype', PType),
    ('address', int),
    ('depth', int),
    ('isGlobal', bool)
])

MethodRecord = NamedTuple('MethodRecord', [
    ('returnType', CType),
    ('signature', List[CType]),
    ('label', Label),
])

class SymbolNode:
    '''A tree class used to store a program's scopes and their symbols.'''
    def __init__(self, parent: Optional['SymbolNode']) -> None:
        # Parent has to be a SymbolNode
        self.parent = parent
        self.children = [] # type: List[SymbolNode]
        self.symbols = {} # type: Dict[str, Union[VariableRecord, MethodRecord]]
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
        Used to help determine the address for variables defined in a Statement inside a method.
        '''
        varSpace = 0
        node = self
        while(node.depth != 0):
            varSpace += node.varSpace
            node = node.parent
        return varSpace

    def max_var_space(self) -> int:
        '''
        Get the maximum amount of variable space this scope uses at a single time (downwards recusive).
        Used to determine the minimum amount of space that needs to be set aside on the stack before the
        stack can be used for evaluating expressions.
        '''
        childMaxVarSpace = 0
        for c in self.children:
            childMaxVarSpace = max(childMaxVarSpace, c.max_var_space())
        # No children: Own var space is the maximum.
        return childMaxVarSpace + self.varSpace

    def check_repeat(self, name:str) -> bool:
        '''Returns whether or not a symbol of that name is already defined in the *current* scope.'''
        return name in self.symbols

    def register(self, name:str, record : Union[VariableRecord, MethodRecord]) -> None:
        '''Register a new record to the current scope.'''
        self.symbols[name] = record

    def find(self, name:str) -> Union[VariableRecord, MethodRecord]:
        '''Search upwards through the tree to find the first symbol by the given name.

        Returns None if the symbol is not found.'''
        node = self
        while node is not None:
            if name in node.symbols:
                return node.symbols[name]
            node = node.parent
        return None

class Environment:
    '''An object holding a dictionary of all declared variables reachable from a certain scope.'''

    def __init__(self):
        self.symbols = SymbolNode(None)

    def deepen(self):
        '''Deepens the symbol scope.'''
        newScope = SymbolNode(self.symbols)
        self.symbols = newScope

    def undeepen(self):
        '''Undeepens the symbol scope: All symbols defined in this level drop out of scope.'''
        self.symbols = self.symbols.parent

    def alloc(self, size: int) -> int:
        '''Allocates a spot of size `size` to the current scope.'''
        addr = self.symbols.frame_var_space()
        self.symbols.varSpace += size
        return addr

    def register_variable(self, name : str, ctype : CType) -> None:
        '''Registers a variable to the current scope'''

        # Check if the symbol is already defined in the current scope
        if(self.symbols.check_repeat(name)):
            raise ValueError('Repeated declaration of symbol "{}"'.format(name))

        # Make a new variable record and register it to the current scope.
        ptype = ctype.ptype()
        isGlobal = (self.symbols.depth == 0)
        # Address works differently for global/local variables
        # TODO: or does it really?
        address = self.alloc(ptype.size())
        if not isGlobal:
            address += 5

        print('registered var {} at depth {} at address {}'.format(name, self.symbols.depth, address))

        self.symbols.register(name, VariableRecord(ctype, ptype, address, self.symbols.depth, isGlobal))

    def get_var(self, name : str) -> VariableRecord:
        '''Get the record of the specified variable, if it exists.'''

        var = self.symbols.find(name)
        if not var:
            raise ValueError('Use of undefined variable "{}"'.format(name))
        if isinstance(var, MethodRecord):
            raise ValueError('Attempted to use symbol "{}" as a variable when it is a function.'.format(name))
        return var

    def register_function(self, name : str, returnType : CType, signature : List[CType]) -> Label:
        '''Registers a function to the global scope and get its label.'''

        # Check if the symbol is already defined in the current scope
        if(self.symbols.check_repeat(name)):
            raise ValueError('Repeated declaration of symbol "{}"'.format(name))

        # Make a method record and register it
        label = Label('f_{}'.format(name))
        self.symbols.register(name, MethodRecord(returnType, signature, label))
        return label

    def get_func(self, name : str) -> MethodRecord:
        '''Get the record of the specified function, if it exists.'''

        func = self.symbols.find(name)
        if not func:
            raise ValueError('Use of undefined function "{}"'.format(name))
        if isinstance(func, VariableRecord):
            raise ValueError('Attempted to use symbol "{}" as a function when it is a variable.'.format(name))
        return func
