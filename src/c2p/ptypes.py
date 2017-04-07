class PType:
    def __init__(self, letter: str) -> None:
        self.letter = letter

    def size(self):
        # are these ever larger than 1?
        return 1

    def __repr__(self):
        return self.letter

class PNumericType(PType):
    pass

PAddress = PType('a')
PBoolean = PType('b')
PCharacter = PType('c')
PInteger = PNumericType('i')
PReal = PNumericType('r')
