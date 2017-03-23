import sys
import c2p

def run(argv):
    i = c2p.instructions.Add(c2p.ptypes.Real)
    print(i.emit())

if __name__ == '__main__':
    run(sys.argv)
