import sys
import c2p

from c2p.grammar.ctypes import *

def run(argv):
    i = c2p.instructions.Add(c2p.ptypes.PReal)
    print(i.emit())

    assert CVoid() == CVoid()
    assert CVoid() != CInt()
    assert CPointer(CVoid()) == CPointer(CVoid())
    assert CPointer(CVoid()) != CPointer(CInt())
    assert CPointer(CVoid()) != CVoid()

if __name__ == '__main__':
    run(sys.argv)
