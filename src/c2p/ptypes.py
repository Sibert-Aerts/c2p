class PType:
    def __init__(self, letter: str) -> None:
        self.letter = letter

class PNumericType(PType):
    pass

Address = PType('a')
Boolean = PType('b')
Character = PType('c')
Integer = PNumericType('i')
Real = PNumericType('r')
