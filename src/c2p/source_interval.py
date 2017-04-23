class SourceLocation:
    def __init__(self, line: int, column: int) -> None:
        self.line = line
        self.column = column

class SourceInterval:
    def __init__(self, start: SourceLocation, stop: SourceLocation) -> None:
        self.start = start
        self.stop = stop
