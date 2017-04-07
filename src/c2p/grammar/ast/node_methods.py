from .node import *
from c2p.grammar.ctypes import *

# CType synthesis from declarator 'types':
# int *x, y[]   →   (CPointer(CInt), "x") and (CArray(CInt), "y")
# So we need to tell each type of Declarator how to make a CType.

def identdecl_to_ctype(self, declType : CType) -> (CType, str):
    return (declType, self.identifier.name)

IdentifierDeclarator.to_ctype = identdecl_to_ctype

def ptrdecl_to_ctype(self, declType : CType) -> (CType, str):
    innerType, name = self.inner.to_ctype(declType)
    return (CPointer(innerType), name)

PointerDeclarator.to_ctype = ptrdecl_to_ctype

def constdecl_to_ctype(self, declType : CType) -> (CType, str):
    innerType, name = self.inner.to_ctype(declType)
    return (CConst(innerType), name)

ConstantDeclarator.to_ctype = constdecl_to_ctype

def arrdecl_to_ctype(self, declType : CType) -> (CType, str):
    innerType, name = self.inner.to_ctype(declType)
    return (CArray(innerType), name)

ArrayDeclarator.to_ctype = arrdecl_to_ctype