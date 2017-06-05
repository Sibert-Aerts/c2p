from typing import Any, Dict, Iterable, List, NamedTuple, Optional, Union
from c2p.ptypes import *
from c2p.grammar.ctypes import *
from c2p import instructions
from c2p.instructions.branch import Label
from c2p.codegen.code_node import CodeNode
from c2p.codegen.error import SemanticError
from c2p.source_interval import SourceInterval

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
    ('defined', bool),
])

class Scope:
    '''A mapping of symbols (names) to variable/function records, which may
    itself have parent or child scopes.'''
    def __init__(self, parent: Optional['Scope']) -> None:
        self.parent = parent
        self.children = []  # type: List[Scope]
        self.symbols = {}   # type: Dict[str, Union[VariableRecord, FunctionRecord]]
        # varSpace is the amount of space the variables defined in this scope take up
        # varSpace is NOT an address
        self.varSpace = 0
        self.maxVarSpace = 0

        # These are only used in for/while loop scopes.
        self.isLoop = False
        self.breakLabel = None      # type: str
        self.continueLabel = None   # type: str

        if parent is None:
            self.depth = 0
        else: # Calculate depth, append self to the parent
            self.depth = parent.depth + 1
            self.parent.children.append(self)

        # Find the scope that has to store all your local variables in a frame
        self.varScope = self
        while self.varScope.depth > 1:
            self.varScope = self.varScope.parent

    def frame_var_space(self) -> int:
        '''
        Get the total space of all variables reachable by this scope (upwards recursive),
        that are stored in the current frame (so no globals).
        Used to help determine the address for variables defined in a Statement inside a function.
        '''
        varSpace = self.varSpace
        scope = self.parent
        while scope and scope.depth != 0:
            varSpace += scope.varSpace
            scope = scope.parent
        return varSpace

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
        offset = self.frame_var_space()
        self.varSpace += size
        self.varScope.maxVarSpace = max(self.varScope.maxVarSpace, offset + size)
        return offset

    def _get_variable(self, name: str, where: SourceInterval) -> VariableRecord:
        variable = self.find(name)
        if not variable:
            raise SemanticError('Use of undefined variable "{}"'.format(name), where)
        if isinstance(variable, FunctionRecord):
            raise SemanticError('Attempted to use symbol "{}" as a variable when it is a function.'.format(name), where)
        return variable

    def _get_function(self, name: str, where: SourceInterval) -> FunctionRecord:
        function = self.find(name)
        if not function:
            raise SemanticError('Use of undefined function "{}"'.format(name), where)
        if isinstance(function, VariableRecord):
            raise SemanticError('Attempted to use symbol "{}" as a function when it is a variable.'.format(name), where)
        return function

    def _register_variable(self, name: str, ctype: CType, where: SourceInterval) -> None:
        # Check if the symbol is already defined in the current scope
        if name in self.symbols:
            raise SemanticError('Repeated declaration of symbol "{}"'.format(name), where)

        # Make a new variable record and register it to the current scope.
        address = self._alloc(ctype.size())
        # The size of the stack frame differs between global/local scope
        isGlobal = (self.depth == 0)
        address += 9 if isGlobal else 5

        self.symbols[name] = VariableRecord(ctype, ctype.ptype(), address, self.depth, isGlobal)

    def _register_function(self, name: str, returnType: CType, signature: List[CType], where: SourceInterval, isDefinition: bool = False) -> Label:
        assert self.depth == 0, 'register_function not at global scope'

        # Check if the symbol is already defined in the current scope
        if name in self.symbols:
            raise SemanticError('Repeated declaration of symbol "{}"'.format(name), where)

        # Make a function record and register it
        label = Label('f_{}'.format(name))
        self.symbols[name] = FunctionRecord(returnType, signature, label, isDefinition)
        return label

    def _set_as_loop(self, br : str, cont : str) -> None:
        self.isLoop = True
        self.breakLabel = br
        self.continueLabel = cont

    def _find_loop(self) -> Optional['Scope']:
        scope = self
        while scope:
            if scope.isLoop:
                return scope
            scope = scope.parent
        return None

class Environment:
    '''Manages a Scope, and global string literals.'''

    def __init__(self) -> None:
        self.scope = Scope(None)
        self.heap_pointer = 0
        self.string_literals = []   # type: List[str]
        self.returnType = None      # type: Optional[CType]

    def deepen(self) -> None:
        '''Deepens the symbol scope.'''
        newScope = Scope(self.scope)
        self.scope = newScope

    def undeepen(self) -> None:
        '''Undeepens the symbol scope: All symbols defined in this level drop out of scope.'''
        self.scope = self.scope.parent

    def add_string_literal(self, string: str) -> int:
        string += '\0'
        self.string_literals.append(string)
        self.heap_pointer -= len(string)
        return self.heap_pointer

    def string_literal_code(self) -> CodeNode:
        '''Emit code that allocates string literals on the heap.'''
        total_size = -self.heap_pointer
        code = CodeNode()
        if total_size == 0:
            return code

        code.add(instructions.Ldc(PAddress, 0))
        code.add(instructions.Ldc(PInteger, total_size))
        code.add(instructions.New())
        ptr = self.heap_pointer
        for string in self.string_literals[::-1]:
            for character in string:
                code.add(instructions.Ldc(PCharacter, ord(character)))
                code.add(instructions.Sro(PCharacter, ptr))
                ptr += 1
        return code

    def alloc(self, size: int) -> int:
        '''Allocates a spot of size `size` to the current scope, returning its address.'''
        return self.scope._alloc(size)

    def get_variable(self, name: str, where: SourceInterval) -> VariableRecord:
        '''Retrieve a variable record from this scope or above, or throw a SemanticError.'''
        return self.scope._get_variable(name, where)

    def get_function(self, name: str, where: SourceInterval) -> FunctionRecord:
        '''Retrieve a function record from this scope or above, or throw a SemanticError.'''
        return self.scope._get_function(name, where)

    def register_variable(self, name: str, ctype: CType, where: SourceInterval) -> None:
        '''Registers a variable to the current scope.'''
        self.scope._register_variable(name, ctype, where)

    def register_function(self, name: str, returnType: CType, signature: List[CType], where: SourceInterval, isDefinition: bool = False) -> Label:
        '''Registers a function to the (global) scope and get its label.'''
        return self.scope._register_function(name, returnType, signature, where, isDefinition)

    def declare_function(self, name: str, returnType: CType, signature: List[CType],
            where: SourceInterval, isDefinition: bool = False) -> FunctionRecord:
        '''Registers a function to the (global) scope if it does not yet exist, and get its record.'''
        try:
            fr = self.get_function(name, where)
        except SemanticError as e:
            self.register_function(name, returnType, signature, where, isDefinition)
            return self.get_function(name, where)

        # OK, it already existed. Make sure we aren't redefining or conflicting.
        if fr.returnType != returnType or fr.signature != signature:
            raise SemanticError('Conflicting declaration of "%s"!' % name, where)
        if isDefinition and fr.defined:
            raise SemanticError('Redefinition of "%s"!' % name, where)
        self.scope.symbols[name] = fr = fr._replace(defined=isDefinition)
        return fr

    def set_as_loop(self, br : Label, cont : Label) -> None:
        '''Defines the current scope as a loop, and registers its 'break' and 'continue' labels.'''
        self.scope._set_as_loop(br.label, cont.label)

    def find_loop(self) -> Optional['Scope']:
        '''Search upwards through the scope tree (including current scope) to find the first scope defined as a loop.
        Returns None if no such scope is found.'''
        return self.scope._find_loop()