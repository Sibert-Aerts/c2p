class PType:
    def __init__(self, letter: str) -> None:
        self.letter = letter

class PNumericType(PType):
    pass

PAddress = PType('a')
PBoolean = PType('b')
PCharacter = PType('c')
PInteger = PNumericType('i')
PReal = PNumericType('r')
