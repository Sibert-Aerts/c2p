from c2p.ptypes import *
from c2p.grammar.ctypes import *
from typing import Any, List, NamedTuple, Optional, Union
from c2p.instructions.branch import Label
import copy


VariableRecord = NamedTuple('VariableRecord', [
    ('ctype', CType),
    ('ptype', PType),
    ('address', int),
    ('depth', int),
])


FunctionRecord = NamedTuple('FunctionRecord', [
    ('returnType', CType),
    ('signature', List[CType]),
    ('label', Label),
])

class Environment:
    '''An object holding a dictionary of all declared variables reachable from a certain scope.'''

    def __init__(self):
        self.symbols = {}
        self.depth = 0
        self.offset = 0

    def deepen(self):
        '''Returns a copy of the current Environment, to be used in a deeper scope'''
        clone = copy.deepcopy(self)
        clone.depth = self.depth + 1
        return clone

    def stack_alloc(self, size : int) -> int:
        '''Allocates a spot of size `size` to the stack for the rest of the scope's duration'''
        addr = self.offset
        self.offset += size
        return addr
    
    def register_variable(self, name : str, ctype : CType) -> None:
        '''Registers a variable to the current scope, and all nested scopes within it
        Overrides existing variables of the same name if they were defined in a higher scope'''
        
        try:
            s = self.symbols[name]
            if isinstance(s, FunctionRecord):
                raise ValueError('Attempted to declare symbol "{}" as a variable when it is a function.'.format(name))
            if s.depth == self.depth:
                raise ValueError('Repeated declaration of variable "{}"'.format(name))
        except KeyError:
            pass
        except ValueError as e:
            raise e

        ptype = ctype.ptype()
        address = self.stack_alloc(ptype.size())
        self.symbols[name] = VariableRecord(ctype, ptype, address, self.depth)

    def get_var(self, name : str) -> VariableRecord:
        '''Get the record of the specified variable, if it exists.'''
        try:
            var = self.symbols[name]
            if isinstance(var, FunctionRecord):
                raise ValueError('Attempted to use symbol "{}" as a variable when it is a function.'.format(name))
            return var
        except KeyError:
            raise ValueError('Use of nonexistent variable "{}"'.format(name))
        except ValueError as e:
            raise e
    
    def register_function(self, name : str, returnType : CType, signature : List[CType]) -> Label:
        '''Registers a function to the global scope and get its label.'''
        
        try:
            s = self.symbols[name]
            raise ValueError('Repeated declaration of function "{}"'.format(name))
        except KeyError:
            pass
        except ValueError as e:
            raise e

        label = Label('f_{}'.format(name))
        self.symbols[name] = FunctionRecord(returnType, signature, label)
        return label

    def get_func(self, name : str) -> FunctionRecord:
        '''Get the record of the specified function, if it exists.'''
        try:
            func = self.symbols[name]
            if isinstance(func, VariableRecord):
                raise ValueError('Attempted to use symbol {} as a function when it is a variable.'.format(name))
            return func
        except KeyError:
            raise ValueError('Use of nonexistent function {}'.format(name))
        except ValueError as e:
            raise e